from pydantic import BaseModel
from typing import Any


class CodingAgentResponse(BaseModel):
    executableCode: str


class StateStatsScraperCodeExecutionResponse(BaseModel):
    typicalHomeValue: int
    oneYearValueChange: float
    dateThrough: str
    housingMarketOverview: list[str]
    anyOtherPropertyRelatedInfo: dict[str, Any]
