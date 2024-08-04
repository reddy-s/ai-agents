import logging
import torch

from transformers import AutoModelForCausalLM, AutoTokenizer
from ..abstract_wrapper import AbstractWrapper

logger = logging.getLogger(__name__)


class Codellama(AbstractWrapper):
    def __init__(self, device: torch.device, identifier: str = "meta-llama/CodeLlama-7b-Instruct-hf",):
        super().__init__(identifier)

        self._tokenizer = AutoTokenizer.from_pretrained(self.identifier)

        self._model = AutoModelForCausalLM.from_pretrained(self.identifier).to(device)
        self._device = device

    @property
    def model(self) -> torch.nn.Module:
        return self._model

    @property
    def tokenizer(self):
        return self._tokenizer

    def encode(self, text: str) -> tuple[torch.Tensor, torch.Tensor]:
        inputs = self._tokenizer(text, return_tensors="pt")
        return inputs['input_ids'].to(self._device), inputs['attention_mask'].to(self._device)

    def decode(self, tokens: torch.Tensor) -> str:
        return self._tokenizer.decode(tokens, skip_special_tokens=True)

    def apply_prompt_template(self, messages: list[dict]) -> str:
        return self._tokenizer.apply_chat_template(
            conversation=messages,
            tokenize=False,
            skip_special_tokens=True,
        )

    def generate(
        self,
        messages: list[dict],
        max_new_tokens: int = 256,
        do_sample: bool = True,
        temperature: float = 0.6,
        top_p: float = 0.9,
    ) -> dict[str, str]:
        prompt = self.apply_prompt_template(messages)

        input_ids, attention_mask = self.encode(prompt)
        output = self._model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            temperature=temperature,
            top_p=top_p,
            num_return_sequences=1,
            pad_token_id=self._tokenizer.eos_token_id
        )
        input_length = input_ids.shape[-1]
        return {
            "role": "assistant",
            "content": self.decode(output[0, input_length:])
        }
