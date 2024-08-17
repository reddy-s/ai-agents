import logging

from aicraft.tools.executor import SQLExecutor
from dotenv import load_dotenv
import pandas as pd
from aicraft.types import VisualisationType
from aicraft.tools.tools import ToolHandler
from typing import Any

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_most_preferred_counties_in_a_state_last_month(
    state_id: str, last_yyyymm: int
) -> tuple[pd.DataFrame, str, VisualisationType, dict[str, Any]]:
    """
    Helps in getting the most preferred or most popular or hottest counties in a state which can help with understanding
    which counties to live in. It takes the 2 character state_id (eg: NJ, OH) and the last_yyyymm (eg: 202208, 202406)
    as input and returns the dataframe of the top preference / popularity / hotness scores for counties in that state
    and the visualisation type
    """
    query = f"""
        SELECT
            TRIM(INITCAP(SPLIT_PART(county_name, ',', 1))) AS "County",
            ROUND(hotness_score::numeric, 2) AS "Hotness"
        FROM hobu.county_market_hotness
        WHERE state_id = '{state_id}' AND
              yyyymm = {last_yyyymm}
        ORDER BY hotness_score DESC;
    """
    df = SQLExecutor.execute(query)
    return (
        df,
        f"Hotness Scores per county in {state_id} for {last_yyyymm}",
        VisualisationType.BAR,
        {"x": "County", "y": ["Hotness"]},
    )


class HobuTools(ToolHandler):
    def __init__(self):
        super().__init__(
            {
                "get_most_preferred_counties_in_a_state_last_month": get_most_preferred_counties_in_a_state_last_month
            }
        )
