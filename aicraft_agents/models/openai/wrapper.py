import logging

from openai import OpenAI
from openai.types.chat import ChatCompletion
from ..abstract_wrapper import AbstractWrapper

logger = logging.getLogger(__name__)


class GPT(AbstractWrapper):
    def __init__(self, identifier: str = "gpt-4o"):
        self.identifier = identifier
        self._client = OpenAI()

    def generate(
        self,
        messages: list[dict],
        max_new_tokens: int = 256,
        do_sample: bool = True,
        temperature: float = 0.6,
        top_p: float = 0.9,
    ) -> dict[str, str]:
        response: ChatCompletion = self._client.chat.completions.create(
            model=self.identifier,
            messages=messages,
            max_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
        )
        return {
            "role": response.choices[0].message.role,
            "content": response.choices[0].message.content
        }
