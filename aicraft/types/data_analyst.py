from enum import Enum
from typing import List
from pydantic import BaseModel
from .analysers import State


class VisualisationType(Enum):
    MAP = "map"
    TABLE = "table"
    BAR = "bar"
    LINE = "line"
    AREA = "area"
    SCATTER = "scatter"


class DataAnalystResponseItem(BaseModel):
    visualisationType: list[VisualisationType] = []
    sqlQuery: str = ""

    class Config:
        arbitrary_types_allowed = True


class DataAnalystResponse(BaseModel):
    stateCode: str = ""
    countyName: str = ""
    queries: List[DataAnalystResponseItem] = []

    class Config:
        arbitrary_types_allowed = True
