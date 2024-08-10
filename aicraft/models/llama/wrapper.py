import logging

from ..abstract import CPPInferenceAbstract
from ...types import InferenceConfig

logger = logging.getLogger(__name__)


class LLaMa(CPPInferenceAbstract):
    def __init__(
        self,
        identifier: str = "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF",
        file_suffix: str = "*Q8_0.gguf",
        context_length: int = 4096,
        verbose: bool = False,
        n_gpu_layers: int = -1,
    ):
        super().__init__(
            InferenceConfig(
                identifier=identifier,
                file_suffix=file_suffix,
                verbose=verbose,
                n_gpu_layers=n_gpu_layers,
                n_ctx=context_length,
            )
        )
