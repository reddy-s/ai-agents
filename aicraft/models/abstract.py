import logging
import json
from llama_cpp import Llama, ChatCompletionRequestResponseFormat

from typing import Any
from typing import Iterator

from ..types import (
    InferenceRequest,
    InferenceResponse,
    InferenceConfig,
    FunctionCallRequest,
    FunctionCallResponse,
    FunctionCall,
)

logger = logging.getLogger(__name__)


class CPPInferenceAbstract:
    def __init__(self, config: InferenceConfig):
        self._config = config
        self._model = Llama.from_pretrained(
            repo_id=self._config.identifier,
            filename=self._config.file_suffix,
            n_gpu_layers=self._config.n_gpu_layers,
            verbose=self._config.verbose,
            n_ctx=self._config.n_ctx,
            chat_format=self._config.chat_format,
        )

    @property
    def config(self) -> InferenceConfig:
        return self._config

    @property
    def model(self) -> Any:
        return self._model

    def generate(self, request: InferenceRequest) -> InferenceResponse:
        response = self.model.create_chat_completion(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_new_tokens,
            top_p=request.top_p,
            response_format=ChatCompletionRequestResponseFormat(
                type="json_object",
                schema=request.response_format.schema(),
            ),
        )
        return InferenceResponse(
            role=response["choices"][0]["message"]["role"],
            content=request.response_format(
                **json.loads(response["choices"][0]["message"]["content"])
            ),
        )

    def stream(self, request: InferenceRequest) -> Iterator[str]:
        output = self.model.create_chat_completion(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_new_tokens,
            top_p=request.top_p,
            stream=True,
        )
        for chunk in output:
            content = chunk["choices"][0]["delta"].get("content", None)
            if content:
                yield content

    def action(self, request: FunctionCallRequest) -> FunctionCallResponse:
        response = self.model.create_chat_completion(
            messages=request.messages,
            tools=request.tools,
            tool_choice=request.tool_choice,
        )

        calls = []
        if "tool_calls" not in response["choices"][0]["message"]:
            return FunctionCallResponse(
                role=response["choices"][0]["message"]["role"], calls=calls
            )

        for call in response["choices"][0]["message"]["tool_calls"]:
            calls.append(
                FunctionCall(
                    name=call["function"]["name"],
                    arguments=json.loads(call["function"]["arguments"]),
                )
            )

        return FunctionCallResponse(
            role=response["choices"][0]["message"]["role"], calls=calls
        )

    def __call__(self, request: InferenceRequest) -> InferenceResponse:
        return self.generate(request)
