from ..abstract import AbstractAgent
from ...models import LLaMa
from ...types import PromptType


class EstateAgent(AbstractAgent):
    def __init__(self, template_folder: str):
        super().__init__(
            LLaMa.get_or_create_instance(),
            {
                "role": "system",
                "content": "",
            },
            template_folder,
            PromptType.ESTATE_AGENT_SERVICE_DESK,
        )
