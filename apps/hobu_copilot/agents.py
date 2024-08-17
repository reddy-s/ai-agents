from typing import Iterator

from aicraft.agents import (
    EstateAgent,
    PreferenceAnalysingAgent,
    DataAnalystAgent,
    ActionCallingAgent,
)
from aicraft.types import (
    InferenceRequest,
    InferenceResponse,
    ChatGenerationResponse,
    HobuCustomerConversationPreference,
    DataAnalystResponse,
    FunctionCallRequest,
    FunctionCallResponse,
)
from tools import HobuTools


class Planner:
    def __init__(self, template_folder: str):
        self.agent = EstateAgent(template_folder)
        self.identifier = self.agent.identifier

    def planner_iter(self, messages: list[dict], state: dict = {}) -> Iterator[str]:
        return self.agent.stream(
            InferenceRequest(messages=messages, response_format=ChatGenerationResponse),
            state,
        )


class ConversationAnalyser:
    def __init__(self, template_folder: str):
        self.agent = PreferenceAnalysingAgent(template_folder)
        self.identifier = self.agent.identifier

    def analyse(self, messages: list[dict], state: dict = {}) -> InferenceResponse:
        return self.agent(
            InferenceRequest(
                messages=messages, response_format=HobuCustomerConversationPreference
            ),
            state,
        )


class DataAnalyst:
    def __init__(self, template_folder: str):
        self.agent = DataAnalystAgent(template_folder)
        self.identifier = self.agent.identifier

    def analyse(self, messages: list[dict], state: dict = {}) -> InferenceResponse:
        return self.agent(
            InferenceRequest(messages=messages, response_format=DataAnalystResponse),
            state,
        )


class ActionCaller:
    def __init__(self, template_folder: str):
        self.agent = ActionCallingAgent(template_folder)
        self.identifier = self.agent.identifier

    def call(
        self, messages: list[dict], tools: list[dict], state: dict = {}
    ) -> FunctionCallResponse:
        return self.agent.action(
            FunctionCallRequest(messages=messages, tools=tools, tool_choice="auto"),
            state,
        )
