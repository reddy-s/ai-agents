from ..abstract import AbstractAgent
from ...models import LLaMa, DeepSeek
from ...types import PromptType


class PreferenceAnalysingAgent(AbstractAgent):
    def __init__(self, template_folder: str):
        super().__init__(
            DeepSeek(),
            {
                "role": "system",
                "content": "",
            },
            template_folder,
            PromptType.PREFERENCE_ANALYSIS,
        )
