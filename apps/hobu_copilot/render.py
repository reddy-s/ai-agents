import os
from typing import Iterator, Union
import logging

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
    VisualisationType,
    DataAnalystResponseItem,
    FunctionCallResponse,
)
from tools import HobuTools

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
                dialog.code(e.content)

    @staticmethod
    def render_stream_in_dialogue(
        streaming_iter: Iterator[str], model: str, dialogue: DeltaGenerator
    ) -> Element:
        response = dialogue.write_stream(streaming_iter)
        return Element(content_type=ContentType.MARKDOWN, content=response, model=model)

    @staticmethod
    def tool_choices(
        choices: FunctionCallResponse,
        tools: HobuTools,
        dialogue: DeltaGenerator,
        model: str,
    ) -> list[Element]:
        elements = []
        try:
            for call in choices.calls:
                df, desc, viz_type, config = tools.execute_tool(
                    call.name, **call.arguments
                )
                if len(df) > 0:
                    if desc is not None:
                        dialogue.markdown(f"## {desc}")
                    if VisualisationType.LINE == viz_type:
                        content_type = ContentType.LINE
                        dialogue.line_chart(df, **config)
                    elif VisualisationType.AREA == viz_type:
                        content_type = ContentType.AREA
                        dialogue.area_chart(df, **config)
                    elif VisualisationType.SCATTER == viz_type:
                        content_type = ContentType.SCATTER
                        dialogue.scatter_chart(df, **config)
                    elif VisualisationType.BAR == viz_type:
                        content_type = ContentType.BAR
                        dialogue.bar_chart(df, **config)
                    elif VisualisationType.TABLE == viz_type:
                        content_type = ContentType.TABLE
                        dialogue.table(df, **config)
                    else:
                        content_type = ContentType.TABLE
                        dialogue.dataframe(df, **config)

                    elements.append(
                        Element(
                            content_type=content_type,
                            content={
                                "config": config,
                                "desc": desc,
                                "func_name": call.name,
                                "arguments": call.arguments,
                            },
                            model=model,
                        )
                    )
            return elements
        except Exception as e:
            logger.info(e)
            return elements
