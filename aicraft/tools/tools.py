import logging
import inspect

from typing import get_type_hints, Any
from dotenv import load_dotenv
import pandas as pd
from aicraft.types import VisualisationType, ToolExecutionResponse

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ToolHandler:

    tools = None

    def __init__(self, tools):
        self.tools = tools

    @staticmethod
    def generate_function_metadata(func):
        func_name = func.__name__

        signature = inspect.signature(func)
        docstring = func.__doc__.strip() if func.__doc__ else ""

        type_hints = get_type_hints(func)

        properties = {}
        required = []

        for param_name, param in signature.parameters.items():
            param_type = type_hints.get(param_name, str)

            if param_type == int:
                json_type = "integer"
            elif param_type == float:
                json_type = "number"
            elif param_type == bool:
                json_type = "boolean"
            else:
                json_type = "string"

            properties[param_name] = {
                "title": param_name.capitalize(),
                "type": json_type,
            }

            required.append(param_name)

        function_metadata = {
            "type": "function",
            "function": {
                "name": func_name,
                "description": docstring,
                "parameters": {
                    "type": "object",
                    "title": func_name,
                    "properties": properties,
                    "required": required,
                },
            },
        }

        return function_metadata

    def get_tools(self) -> list[dict]:
        tools = []
        for func in self.tools.values():
            tools.append(self.generate_function_metadata(func))
        return tools

    def execute_tool(
        self, func_name: str, **kwargs
    ) -> ToolExecutionResponse:
        func = self.tools[func_name]
        return func(**kwargs)
