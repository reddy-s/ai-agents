from pydantic import BaseModel
import pandas as pd
from .data_analyst import VisualisationType
from typing import Any


class ToolExecutionResponse(BaseModel):
    df: pd.DataFrame
    title: str
    viz_type: VisualisationType
    viz_config: dict[str, Any]
    choices: list[dict[str, Any]]

    class Config:
        arbitrary_types_allowed = True
