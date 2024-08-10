import logging

from openai import OpenAI
from openai.types.chat import ChatCompletion
from pydantic import BaseModel
from ...types import InferenceConfig, InferenceRequest, InferenceResponse

from ..abstract import CPPInferenceAbstract

logger = logging.getLogger(__name__)


class GPT(CPPInferenceAbstract):
    def __init__(self, identifier: str = "gpt-4o-mini"):
        self._config = InferenceConfig(
            identifier=identifier,
            file_suffix="NA",
        )
        self._model = OpenAI()

    def generate(self, request: InferenceRequest) -> InferenceResponse:
        response: ChatCompletion = self._model.beta.chat.completions.parse(
            model=self.config.identifier,
            messages=request.messages,
            max_tokens=request.max_new_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            response_format=request.response_format,
        )
        return InferenceResponse(
            role=response.choices[0].message.role,
            content=response.choices[0].message.parsed,
        )

    # def stream(self, request: InferenceRequest) -> Iterator[str]:
    #     output = self.model.create_chat_completion(
    #         messages=request.messages,
    #         temperature=request.temperature,
    #         max_tokens=request.max_new_tokens,
    #         top_p=request.top_p,
    #         stream=True,
    #     )
    #     for chunk in output:
    #         content = chunk["choices"][0]["delta"].get("content", None)
    #         if content:
    #             yield content
