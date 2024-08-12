import os
from typing import Iterator, Union
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from dotenv import load_dotenv
from aicraft.types import (
    Roles,
    Conversation,
    UserMessage,
    AssistantMessage,
    Element,
    ContentType,
)

load_dotenv()


class Renderer:
    user_icon = f"{os.environ.get('HOBU_COPILOT_ASSETS')}/images/static/family.png"
    agent_icon = f"{os.environ.get('HOBU_COPILOT_ASSETS')}/images/static/ai-c.png"
    sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]

    @staticmethod
    def render_chat_history():
        conversation: Conversation = st.session_state.user.conversation
        for message in conversation.messages:
            Renderer.render_message(message)

    @staticmethod
    def render_message(message: Union[UserMessage, AssistantMessage]):
        dialog = st.chat_message(
            name=message.role,
            avatar=(
                Renderer.user_icon
                if message.role == Roles.user.value
                else Renderer.agent_icon
            ),
        )
        for e in message.elements:
            if e.contentType in [ContentType.MARKDOWN, ContentType.TEXT]:
                dialog.markdown(e.content)
            if e.contentType == ContentType.JSON:
                dialog.json(e.content)
            if e.contentType == ContentType.SQL:
                dialog.markdown(f"```sql\n{e.content}```")

    @staticmethod
    def render_stream_in_dialogue(streaming_iter: Iterator[str], model: str, dialogue: DeltaGenerator) -> Element:
        response = dialogue.write_stream(streaming_iter)
        return Element(content_type=ContentType.MARKDOWN, content=response, model=model)
