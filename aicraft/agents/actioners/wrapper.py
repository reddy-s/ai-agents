from ..abstract import AbstractAgent
from ...models import Functionary
from ...types import PromptType


class ActionCallingAgent(AbstractAgent):
    def __init__(self, template_folder: str):
        super().__init__(
            Functionary.get_or_create_instance(),
            {
                "role": "system",
                "content": "",
            },
            template_folder,
            PromptType.ACTION_CALLER,
        )
