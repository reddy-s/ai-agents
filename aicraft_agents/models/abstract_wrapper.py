from abc import ABC, abstractmethod
from typing import Any


class AbstractWrapper(ABC):
    @abstractmethod
    def __init__(self, identifier: str):
        self.identifier = identifier

    @abstractmethod
    def generate(
        self,
        messages: list[dict],
        max_new_tokens: int,
        do_sample: bool,
        temperature: float,
        top_p: float,
    ) -> dict[str, Any]:
        raise NotImplementedError(f"{__class__.__name__}:generate not implemented")
