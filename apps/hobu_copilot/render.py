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
    FunctionCallResponse,
    ToolExecutionResponse
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
    def render_viz(function_name: str, args: dict, tools: HobuTools, dialogue: DeltaGenerator, model: str) -> Element:
        response: ToolExecutionResponse = tools.execute_tool(
            function_name, **args
        )

        if len(response.df) > 0:
            if response.title is not None:
                dialogue.markdown(f"{response.title}")
            if VisualisationType.LINE == response.viz_type:
                content_type = ContentType.LINE
                dialogue.line_chart(response.df, **response.viz_config)
            elif VisualisationType.AREA == response.viz_type:
                content_type = ContentType.AREA
                dialogue.area_chart(response.df, **response.viz_config)
            elif VisualisationType.SCATTER == response.viz_type:
                content_type = ContentType.SCATTER
                dialogue.scatter_chart(response.df, **response.viz_config)
            elif VisualisationType.BAR == response.viz_type:
                content_type = ContentType.BAR
                dialogue.bar_chart(response.df, **response.viz_config)
            elif VisualisationType.TABLE == response.viz_type:
                content_type = ContentType.TABLE
                dialogue.table(response.df, **response.viz_config)
            else:
                content_type = ContentType.TABLE
                dialogue.dataframe(response.df, **response.viz_config)

            return Element(
                content_type=content_type,
                content={
                    "func_name": function_name,
                    "arguments": args,
                },
                model=model,
            )

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
                e = Renderer.render_viz(
                    call.name, call.arguments, tools, dialogue, model
                )
                elements.append(e)
            return elements
        except Exception as e:
            logger.info(e)
            return elements
