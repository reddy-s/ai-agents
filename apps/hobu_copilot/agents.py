from typing import Iterator

from aicraft.agents import EstateAgent, PreferenceAnalysingAgent
from aicraft.types import (
    InferenceRequest,
    InferenceResponse,
    ChatGenerationResponse,
    HobuCustomerConversationPreference,
)


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
