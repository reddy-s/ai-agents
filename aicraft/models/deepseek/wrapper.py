import logging

from ..abstract import CPPInferenceAbstract
from ...types import InferenceConfig

logger = logging.getLogger(__name__)


class DeepSeek(CPPInferenceAbstract):
    _instance = None

    def __init__(
        self,
        identifier: str = "bartowski/DeepSeek-Coder-V2-Lite-Instruct-GGUF",
        file_suffix: str = "*Q8_0.gguf",
        context_length: int = 4096,
        verbose: bool = False,
        n_gpu_layers: int = -1,
    ):
        super().__init__(
            InferenceConfig(
                identifier=identifier,
                file_suffix=file_suffix,
                n_gpu_layers=n_gpu_layers,
                verbose=verbose,
                n_ctx=context_length,
            )
        )

    @classmethod
    def get_or_create_instance(cls):
        if cls._instance is None:
            logger.info("Creating new instance of DeepSeek")
            cls._instance = DeepSeek()
        else:
            logger.info("Returning existing instance of DeepSeek")
        return cls._instance
