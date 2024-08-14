from ..abstract import AbstractAgent
from ...models import LLaMa, DeepSeek
from ...types import PromptType


class WebScrapingAgent(AbstractAgent):
    def __init__(self, template_folder: str):
        super().__init__(
            DeepSeek.get_or_create_instance(),
            {
                "role": "system",
                "content": "",
            },
            template_folder,
            PromptType.WEB_SCRAPING,
        )
