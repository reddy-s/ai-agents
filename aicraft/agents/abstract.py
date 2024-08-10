from typing import Iterator

from ..models.abstract import CPPInferenceAbstract
from ..types import InferenceResponse, InferenceRequest, PromptType
from ..tools.prompts import PromptConstructor


class AbstractAgent:
    def __init__(
        self,
        model: CPPInferenceAbstract,
        instruction: dict,
        template_folder: str,
        prompt_type: PromptType,
    ):
        self.model = model
        self.instruction = instruction
        self.identifier = self.model.config.identifier
        self.prompt_constructor = PromptConstructor.get_or_create_instance(
            template_folder
        )
        self.prompt_method = prompt_type.value

    def _update_prompt_with_state(self, state: dict):
        prompt = getattr(self.prompt_constructor, self.prompt_method)(state)
        self.instruction["content"] = prompt

    def __call__(self, context: InferenceRequest, state: dict) -> InferenceResponse:
        self._update_prompt_with_state(state)
        context.messages.insert(0, self.instruction)
        return self.model.generate(context)

    def stream(self, context: InferenceRequest, state: dict) -> Iterator[str]:
        self._update_prompt_with_state(state)
        context.messages.insert(0, self.instruction)
        return self.model.stream(context)
