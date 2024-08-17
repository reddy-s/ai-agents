import logging

from llama_cpp import Llama
from llama_cpp.llama_tokenizer import LlamaHFTokenizer
from ..abstract import CPPInferenceAbstract
from ...types import InferenceConfig

logger = logging.getLogger(__name__)


class Functionary(CPPInferenceAbstract):
    _instance = None

    def __init__(
        self,
        identifier: str = "meetkai/functionary-small-v2.2-GGUF",
        file_suffix: str = "*q8_0.gguf",
        context_length: int = 4096,
        verbose: bool = False,
        n_gpu_layers: int = -1,
    ):
        self._config = InferenceConfig(
            identifier=identifier,
            file_suffix=file_suffix,
            verbose=verbose,
            n_gpu_layers=n_gpu_layers,
            n_ctx=context_length,
            chat_format="functionary-v2",
        )

        self._model = Llama.from_pretrained(
            repo_id=self._config.identifier,
            filename=self._config.file_suffix,
            n_gpu_layers=self._config.n_gpu_layers,
            n_ctx=self._config.n_ctx,
            verbose=self._config.verbose,
            chat_format=self._config.chat_format,
            tokenizer=LlamaHFTokenizer.from_pretrained(self._config.identifier),
        )

    @classmethod
    def get_or_create_instance(cls):
        if cls._instance is None:
            logger.info("Creating new instance of DeepSeek")
            cls._instance = Functionary()
        else:
            logger.info("Returning existing instance of DeepSeek")
        return cls._instance
