import logging

from aicraft.tools.executor import SQLExecutor
from dotenv import load_dotenv
from aicraft.types import VisualisationType, ToolExecutionResponse, State
from aicraft.tools.tools import ToolHandler

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_most_preferred_counties_in_a_state_last_month(
    state_id: str, last_yyyymm: int
) -> ToolExecutionResponse:
    """
    Helps in getting the most preferred or most popular or hottest counties in a state which can help with understanding
    which counties to live in. It takes the 2 character state_id (eg: NJ, OH) and the last_yyyymm (eg: 202208, 202406)
    as input and returns the dataframe of the top preference / popularity / hotness scores for counties in that state
    and the visualisation type

    Arguments:
    - state_id: should be 2 character state abbreviation in uppercase eg: NY, CA
    - last_yyyymm: should be the year and month in yyyymm format eg: 202208, 202406
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
    logger.info(f"Executing query: \n{query}")
    df = SQLExecutor.execute(query)
    return ToolExecutionResponse(
        df=df,
        title=f"##### Hotness Score per county in *:orange[{state_id}]* for *:blue[{last_yyyymm}]*",
        viz_type=VisualisationType.BAR,
        viz_config={"x": "County", "y": ["Hotness"]},
        choices=[],
    )


def get_top_addresses_by_hotness(state_id: str, last_yyyymm: int) -> ToolExecutionResponse:
    """
    Retrieves the top N hottest/popular Addresses in a state for the specified month. This can help identify which specific
    neighborhoods or areas are most in-demand.

    Arguments:
    - state_id: should be 2 character state abbreviation in uppercase eg: NY, CA
    - last_yyyymm: should be the year and month in yyyymm format eg 202208, 202406
    """
    query = f"""
        SELECT
            concat(address, ', 0', postcode) AS "Address",
            ROUND(hotness_score::numeric, 2) AS "Hotness"
        FROM hobu.zipcode_market_hotness
        WHERE state_id = '{state_id}' AND
              yyyymm = {last_yyyymm}
        ORDER BY hotness_score DESC
        LIMIT 10;
    """
    logger.info(f"Executing query: \n{query}")
    df = SQLExecutor.execute(query)
    return ToolExecutionResponse(
        df=df,
        title=f"##### Top *:blue[10]* Hottest Address in *:orange[{state_id}]* for *:blue[{last_yyyymm}]*",
        viz_type=VisualisationType.BAR,
        viz_config={"x": "Address", "y": ["Hotness"]},
        choices=[],
    )


def get_property_days_on_market_trend_county_level(state_id: str, county_id: str) -> ToolExecutionResponse:
    """
    Retrieves the trend of median days on market for a specific county over a given time period. This provides insight
    into how quickly properties are being sold in a county over time.

    Arguments:
    - state_id: should be 2 character state abbreviation in uppercase eg: NY, CA
    - county_id: should be the name of the county in uppercase eg: SOMERSET, SHAWANO, RICHMOND
    """
    county_id = county_id.upper().replace(" COUNTY", "").strip()
    query = f"""
        SELECT
            yyyymm AS "Year-Month",
            ROUND(median_days_on_market::numeric, 2) AS "Median Days on Market"
        FROM hobu.county_market_hotness
        WHERE state_id = '{state_id}' AND
              county_id = '{county_id}'
        ORDER BY yyyymm;
    """
    logger.info(f"Executing query: \n{query}")
    df = SQLExecutor.execute(query)
    return ToolExecutionResponse(
        df=df,
        title=f"##### Median Days on Market Trend for County *:orange[{county_id}]* in *:blue[{state_id}]*",
        viz_type=VisualisationType.LINE,
        viz_config={"x": "Year-Month", "y": ["Median Days on Market"]},
        choices=[],
    )


def get_top_metros_by_supply_score(last_yyyymm: int, top_n: int = 10) -> ToolExecutionResponse:
    """
    Retrieves the top N metros with the highest supply scores for the specified month. A higher supply score indicates
    faster property sales relative to other metros, indicating potentially high competition in these areas.
    """
    query = f"""
        SELECT
            TRIM(INITCAP(metro_name)) AS "Metro",
            ROUND(supply_score::numeric, 2) AS "Supply Score"
        FROM hobu.metro_market_hotness
        WHERE yyyymm = {last_yyyymm}
        ORDER BY supply_score DESC
        LIMIT {top_n};
    """
    logger.info(f"Executing query: \n{query}")
    df = SQLExecutor.execute(query)
    return ToolExecutionResponse(
        df=df,
        title=f"##### Top *:blue[{top_n}]* Metros by Supply Score for *:blue[{last_yyyymm}]*",
        viz_type=VisualisationType.BAR,
        viz_config={"x": "Metro", "y": ["Supply Score"]},
        choices=[],
    )


def get_median_days_on_market_trend_multiple_states(
        list_of_state_ids: list[str]
) -> ToolExecutionResponse:
    """
    Retrieves the trend of median days on market for multiple states over the last specified number of months.
    The result will have one column per state with the corresponding median days on market values.

    Arguments:
    - list_of_state_ids: should be a list of 2 character state abbreviation in uppercase eg: ["NY", "CA"]
    """
    subqueries = []
    for state_id in list_of_state_ids:
        subquery = f"""
            SELECT
                yyyymm,
                ROUND(median_days_on_market::numeric, 2) AS "{state_id}"
            FROM hobu.county_market_hotness
            WHERE state_id = '{state_id}'
        """
        subqueries.append(subquery)

    # Combine all subqueries using full outer joins
    query = " FULL OUTER JOIN ".join(f"({subq}) AS t{idx}" for idx, subq in enumerate(subqueries))

    # Generate the final query with a common yyyymm
    query = f"""
        SELECT t0.yyyymm AS "Year-Month", {", ".join(f"t{idx}.{state_id}" for idx, state_id in enumerate(list_of_state_ids))}
        FROM {query}
        ORDER BY "Year-Month";
    """
    logger.info(f"Executing query: \n{query}")
    df = SQLExecutor.execute(query)
    return ToolExecutionResponse(
        df=df,
        title=f"##### Median Days on Market Trend for States *:orange[{', '.join(list_of_state_ids)}]*",
        viz_type=VisualisationType.LINE,
        viz_config={"x": "Year-Month", "y": list_of_state_ids},
        choices=[],
    )


def get_hotness_trend_multiple_states(
        list_of_state_ids: list[str]
) -> ToolExecutionResponse:
    """
    Retrieves the trend of hotness scores for multiple states over the last specified number of months.
    The result will have one column per state with the corresponding hotness scores.

    Arguments:
    - list_of_state_ids: should be a list of 2 character state abbreviation in uppercase eg: ["NY", "CA"]
    """
    # Create a subquery for each state to calculate hotness scores
    subqueries = []
    for state_id in list_of_state_ids:
        subquery = f"""
            SELECT
                yyyymm,
                ROUND(hotness_score::numeric, 2) AS "{state_id}"
            FROM hobu.county_market_hotness
            WHERE state_id = '{state_id}'
        """
        subqueries.append(subquery)

    # Combine all sub queries using full outer joins
    query = " FULL OUTER JOIN ".join(f"({subq}) AS t{idx}" for idx, subq in enumerate(subqueries))

    # Generate the final query with a common yyyymm
    query = f"""
        SELECT t0.yyyymm AS "Year-Month", {", ".join(f"t{idx}.{state_id}" for idx, state_id in enumerate(list_of_state_ids))}
        FROM {query}
        ORDER BY "Year-Month";
    """
    logger.info(f"Executing query: \n{query}")
    df = SQLExecutor.execute(query)
    return ToolExecutionResponse(
        df=df,
        title=f"##### Hotness Score Trend for States *:orange[{', '.join(list_of_state_ids)}]*",
        viz_type=VisualisationType.LINE,
        viz_config={"x": "Year-Month", "y": list_of_state_ids},
        choices=[],
    )


class HobuTools(ToolHandler):
    def __init__(self):
        super().__init__(
            {
                "get_most_preferred_counties_in_a_state_last_month": get_most_preferred_counties_in_a_state_last_month,
                "get_top_addresses_by_hotness": get_top_addresses_by_hotness,
                "get_property_days_on_market_trend_county_level": get_property_days_on_market_trend_county_level,
                "get_top_metros_by_supply_score": get_top_metros_by_supply_score,
                "get_median_days_on_market_trend_multiple_states": get_median_days_on_market_trend_multiple_states,
                "get_hotness_trend_multiple_states": get_hotness_trend_multiple_states,
            }
        )
