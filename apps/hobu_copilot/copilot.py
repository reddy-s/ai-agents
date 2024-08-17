import logging
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from concurrent.futures import ThreadPoolExecutor
from constants import Constants
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
    DataAnalystResponse,
    FunctionCallRequest,
)
from agents import Planner, ConversationAnalyser, DataAnalyst, ActionCaller
from tools import HobuTools
from render import Renderer
import time

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
        self.action_caller = ActionCaller(
            os.environ.get("HOBU_COPILOT_PROMPT_TEMPLATES")
        )
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.conversation_pairs = 0
        self.tools = HobuTools()

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
        return st.session_state.user.conversation.prompt_pairs > 0

    def update_preferences(
        self, prompt_messages: list[dict], state: dict
    ) -> tuple[float, Optional[HobuCustomerConversationPreference]]:
        try:
            start_time = time.time()
            logger.info("Interpreting user preferences ...")
            response = self.conversation_analyst.analyse(prompt_messages, state)
            preferences = HobuCustomerConversationPreference(**response.content.dict())
            elapsed_time = round(time.time() - start_time, 1)
            if preferences == HobuCustomerConversationPreference():
                raise ValueError("No preferences interpreted")
            return elapsed_time, preferences
        except TypeError as te:
            logger.info(te)
            return 0.0, None
        except ValidationError as ve:
            logger.info(ve)
            return 0.0, None
        except ValueError as vae:
            logger.info(vae)
            return elapsed_time, None

    def get_insights(
        self, prompt_messages: list[dict], state: dict
    ) -> tuple[float, Optional[DataAnalystResponse]]:
        try:
            start_time = time.time()
            inference_response = self.data_analyst.analyse(prompt_messages, state)
            response = DataAnalystResponse(**inference_response.content.dict())
            elapsed_time = round(time.time() - start_time, 1)
            return elapsed_time, response
        except TypeError as te:
            logger.info(te)
            return 0.0, None
        except ValidationError as ve:
            logger.info(ve)
            return 0.0, None

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
    def enable_insight_generator() -> bool:
        if (
            len(st.session_state.user.preferences.desired_state_in_us) > 0
            or len(st.session_state.user.preferences.counties_interested_in)
            or len(st.session_state.user.preferences.metros_interested_in) > 0
        ):
            return True

        return False

    @staticmethod
    def update_analyst_filter_state() -> dict:
        state = Constants.hotness_tables_metadata
        state["filter_for_state_ids"] = [
            s.name for s in st.session_state.user.preferences.desired_state_in_us
        ]
        state["filter_for_counties"] = [
            c.upper().replace(" COUNTY", "")
            for c in st.session_state.user.preferences.counties_interested_in
        ]
        state["filter_for_metros"] = [
            m for m in st.session_state.user.preferences.metros_interested_in
        ]
        return state

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
        # Picking the right tools
        tools_start_time = time.time()
        tool_choices = self.action_caller.call(
            [
                {
                    "role": Roles.user.value,
                    "content": f"Find tools or function calls which can answer the question: {query}",
                }
            ],
            self.tools.get_tools(),
            Constants.hobu_tools_state_dict,
        )
        tools_elapsed_time = round(time.time() - tools_start_time, 1)
        dialogue.markdown(f"*Action Call Elapsed time*: `{tools_elapsed_time}s`")
        dialogue.json(tool_choices.dict(), expanded=False)

        # Generate assistant response
        _assistant_message = AssistantMessage(
            role=Roles.assistant.value,
            elements=self.generate(
                prompt_messages, self.get_unknown_preferences(), dialogue
            ),
        )

        # Rendering Insights
        if len(tool_choices.calls) > 0:
            Renderer.tool_choices(
                tool_choices, self.tools, dialogue, self.action_caller.identifier
            )
            # _assistant_message.elements.extend(els)

        # Analyse user preferences asynchronously
        try:
            if self.enable_preference_interpreter():
                dialogue.toast("Trying to understanding your preferences ...")
                preferences_future = self.executor.submit(
                    self.update_preferences,
                    prompt_messages,
                    self.get_unknown_preferences(),
                )

                preferences_elapsed_time, preferences = preferences_future.result()
                dialogue.markdown(
                    f"*Preference Estimation Elapsed time*: `{preferences_elapsed_time}s`"
                )
                if preferences is not None:
                    st.session_state.user.preferences = preferences
                    st.toast("Your preferences have been updated")
                    dialogue.json(
                        st.session_state.user.preferences.dict(), expanded=False
                    )
                else:
                    st.toast(
                        "Failed to understand your preferences. Will try again in the next attempt"
                    )
        except Exception as e:
            logger.error(e)
            st.error(
                "Failed to understand your preferences. Will try again in the next attempt"
            )
        # Post-process assistant response
        self.add_message_to_state(_assistant_message)
        # Renderer.render_message(_assistant_message)

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
