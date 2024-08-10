import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import os
from typing import Union
from dotenv import load_dotenv
from pydantic import ValidationError
from aicraft.types import (
    Roles,
    UserState,
    UserMessage,
    AssistantMessage,
    Element,
    ContentType,
    HobuCustomerConversationPreference
)
from agents import Planner, ConversationAnalyser
from render import Renderer

load_dotenv()


class Copilot:
    def __init__(self, context_history: int = 5):
        self.context_history = context_history
        self.planner = Planner(os.environ.get("HOBU_COPILOT_PROMPT_TEMPLATES"))
        self.conversation_analyst = ConversationAnalyser(
            os.environ.get("HOBU_COPILOT_PROMPT_TEMPLATES")
        )

    def generate(self, messages: list[dict], state: dict, dialogue: DeltaGenerator) -> list[Element]:
        elements = []
        e = Renderer.render_stream_in_dialogue(
            self.planner.planner_iter(messages, state), self.planner.identifier, dialogue
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

    def update_preferences(self, prompt_messages: list[dict], state: dict) -> bool:
        try:
            response = self.conversation_analyst.analyse(prompt_messages, state)
            preferences = HobuCustomerConversationPreference(**response.content.dict())
            st.session_state.user.preferences = preferences
            return True
        except TypeError:
            return False
        except ValidationError:
            return False

    def process_prompt(self, query: str):
        _user_message = UserMessage(
            role=Roles.user.value,
            elements=[
                Element(
                    contentType=ContentType.TEXT, content=query, model=Roles.user.value
                )
            ],
        )
        self.add_message_to_state(_user_message)
        Renderer.render_message(_user_message)

        prompt_messages = self.get_prompt_messages(last_n=self.context_history)
        dialogue = st.chat_message(
            name=Roles.assistant.value, avatar=Renderer.agent_icon
        )
        self.update_preferences(prompt_messages, self.get_unknown_preferences())

        _assistant_message = AssistantMessage(
            role=Roles.assistant.value,
            elements=self.generate(
                prompt_messages,
                self.get_unknown_preferences(),
                dialogue
            ),
        )

        dialogue.json(st.session_state.user.preferences.dict(), expanded=False)

        self.add_message_to_state(_assistant_message)

    def handler(self, query: str):
        self.process_prompt(query)

    def run(self):

        st.logo(f"{os.environ.get('HOBU_COPILOT_ASSETS')}/images/static/logo.png")

        if "user" not in st.session_state:
            st.session_state.user = UserState()

        if "user" in st.session_state:
            Renderer.render_chat_history()

        query = st.chat_input("Ask away ...")

        if query:
            self.handler(query)
