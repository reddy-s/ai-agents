import logging
import torch
import transformers

from ..abstract_wrapper import AbstractWrapper

logger = logging.getLogger(__name__)


class Llama3(AbstractWrapper):
    def __init__(self, identifier: str = "meta-llama/Meta-Llama-3-8B-Instruct"):
        self.identifier = identifier
        self._pipeline = transformers.pipeline(
            "text-generation",
            model=self.identifier,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
        )
        self._device = self._pipeline.model.device
        self._terminators = [
            self._pipeline.tokenizer.eos_token_id,
            self._pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]
        self._tokenizer = self._pipeline.tokenizer
        self._model = self._pipeline.model

    @property
    def tokenizer(self):
        return self._tokenizer

    @property
    def model(self) -> torch.nn.Module:
        return self._model

    @property
    def device(self) -> torch.device:
        return self._device

    def generate(
        self,
        messages: list[dict],
        max_new_tokens: int = 256,
        do_sample: bool = True,
        temperature: float = 0.6,
        top_p: float = 0.9,
    ) -> dict[str, str]:
        response = self._pipeline(
            messages,
            max_new_tokens=max_new_tokens,
            eos_token_id=self._terminators,
            do_sample=do_sample,
            temperature=temperature,
            top_p=top_p,
        )
        return response[0]["generated_text"][-1]

    def __call__(
        self,
        messages: list[dict],
        max_new_tokens: int = 256,
        do_sample: bool = True,
        temperature: float = 0.6,
        top_p: float = 0.9,
    ) -> dict[str, str]:
        return self.generate(messages, max_new_tokens, do_sample, temperature, top_p)
