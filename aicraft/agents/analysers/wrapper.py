from ..abstract import AbstractAgent
from ...models import LLaMa, DeepSeek, Qwen
from ...types import PromptType


class PreferenceAnalysingAgent(AbstractAgent):
    def __init__(self, template_folder: str):
        super().__init__(
            LLaMa.get_or_create_instance(),
            {
                "role": "system",
                "content": "",
            },
            template_folder,
            PromptType.PREFERENCE_ANALYSIS,
        )
