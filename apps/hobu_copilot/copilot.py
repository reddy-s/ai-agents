import logging
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import os
from typing import Union, Optional
from dotenv import load_dotenv
from pydantic import ValidationError
from aicraft.types import (
    Roles,
    UserState,
    UserMessage,
    AssistantMessage,
    Element,
    ContentType,
    HobuCustomerConversationPreference,
)
from agents import Planner, ConversationAnalyser, WebScraper
from render import Renderer
import time
from executor import Executor


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Copilot:
    def __init__(self, context_history: int = 5):
        self.context_history = context_history
        self.planner = Planner(os.environ.get("HOBU_COPILOT_PROMPT_TEMPLATES"))
        self.conversation_analyst = ConversationAnalyser(
            os.environ.get("HOBU_COPILOT_PROMPT_TEMPLATES")
        )
        self.web_scraper = WebScraper(os.environ.get("HOBU_COPILOT_PROMPT_TEMPLATES"))
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.code_executor = Executor()
        self.conversation_pairs = 0

    def generate(
        self, messages: list[dict], state: dict, dialogue: DeltaGenerator
    ) -> list[Element]:
        elements = []
        e = Renderer.render_stream_in_dialogue(
            self.planner.planner_iter(messages, state),
            self.planner.identifier,
            dialogue,
        )
        elements.append(e)
        return elements

    @staticmethod
    def add_message_to_state(message: Union[UserMessage, AssistantMessage]):
        st.session_state.user.conversation.add_message(message)

    @staticmethod
    def get_unknown_preferences() -> dict[str, list]:
        return st.session_state.user.preferences.get_preference_status()

    @staticmethod
    def get_prompt_messages(last_n=5) -> list[dict[str, str]]:
        return st.session_state.user.conversation.get_messages_for_prompt(last_n=last_n)

    @staticmethod
    def enable_preference_interpreter() -> bool:
        return st.session_state.user.conversation.prompt_pairs > 1

    def update_preferences(
        self, prompt_messages: list[dict], state: dict
    ) -> tuple[float, Optional[HobuCustomerConversationPreference]]:
        try:
            start_time = time.time()
            logger.info("Interpreting user preferences ...")
            response = self.conversation_analyst.analyse(prompt_messages, state)
            preferences = HobuCustomerConversationPreference(**response.content.dict())
            elapsed_time = round(time.time() - start_time, 1)
            return elapsed_time, preferences
        except TypeError:
            return 0.0, None
        except ValidationError:
            return 0.0, None

    def process_prompt(self, query: str):
        # Register user prompt
        _user_message = UserMessage(
            role=Roles.user.value,
            elements=[
                Element(
                    content_type=ContentType.TEXT, content=query, model=Roles.user.value
                )
            ],
        )
        self.add_message_to_state(_user_message)
        Renderer.render_message(_user_message)

        # Preparing conversation for analysis
        prompt_messages = self.get_prompt_messages(last_n=self.context_history)
        dialogue = st.chat_message(
            name=Roles.assistant.value, avatar=Renderer.agent_icon
        )

        # Understand and respond back to the prompt
        try:
            _assistant_message = AssistantMessage(
                role=Roles.assistant.value,
                elements=self.generate(
                    prompt_messages, self.get_unknown_preferences(), dialogue
                ),
            )

            dialogue.bar_chart(np.random.randn(50, 3))
            # TODO: Add more elements to the message
            self.add_message_to_state(_assistant_message)
        except Exception as e:
            logger.error(e)
            st.button(
                "↻ Try again", on_click=self.handler, type="secondary", args=(query,)
            )

        # Analyse user preferences
        if self.enable_preference_interpreter():
            dialogue.toast("Trying to understanding your preferences ...")
            future = self.executor.submit(
                self.update_preferences, prompt_messages, self.get_unknown_preferences()
            )
            elapsed_time, preferences = future.result()
            if preferences is not None:
                st.session_state.user.preferences = preferences
                dialogue.toast("Preferences updated!")
                dialogue.json(st.session_state.user.preferences.dict(), expanded=False)
                dialogue.markdown(f"*Elapsed time*: `{elapsed_time}s`")
            else:
                dialogue.error(
                    "Failed to understand your preferences. Will try again in the next attempt"
                )

    def scrape_state_stats(self, dialogue: DeltaGenerator):
        # TODO: Used for test only and needs to be cleaned up
        _url = "https://www.zillow.com/home-values/40/nj/"
        dialogue.toast(f"Scraping insights from {_url} ...")
        future = self.executor.submit(self.code_executor.scrape_the_web_page, _url, 3)
        elapsed_time, file_location, conv = future.result()
        dialogue.markdown(
            f"""
            *Elapsed time*: `{elapsed_time}`\n
            *File location*: [{file_location}]({file_location})
        """
        )
        dialogue.json(conv, expanded=False)

    def handler(self, query: str):
        self.process_prompt(query)

    def run(self):
        st.logo(f"{os.environ.get('HOBU_COPILOT_ASSETS')}/images/static/logo.png")

        if "user" not in st.session_state:
            st.session_state.user = UserState()

        Renderer.render_chat_history()

        query = st.chat_input("Ask away ...")
        if query:
            self.handler(query)
