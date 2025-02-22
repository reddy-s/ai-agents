class Constants:
    hotness_tables_metadata = {
        "filter_for_latest_yyyymm": "202407",
        "filter_for_state_ids": [],
        "filter_for_counties": [],
        "filter_for_metros": [],
        "tables": [
            {
                "name": "hobu.county_market_hotness",
                "description": "Contains data related to a United States Countys hotness score, supply score, demand score, days on market and listing prices.",
                "columns": [
                    "yyyymm",
                    "state_id",
                    "county_id",
                    "county_name",
                    "hh_rank",
                    "hotness_rank",
                    "hotness_score",
                    "supply_score",
                    "demand_score",
                    "median_days_on_market",
                    "median_days_on_market_vs_us",
                    "median_days_on_market_month_on_month",
                    "hotness_rank_month_on_month",
                    "median_listing_price",
                    "median_listing_price_vs_us",
                    "median_listing_price_month_on_month",
                ],
            },
            {
                "name": "hobu.metro_market_hotness",
                "description": "Contains data related to a United States Metros hotness score, supply score, demand score, days on market and listing prices.",
                "columns": [
                    "yyyymm",
                    "state_id",
                    "metro_name",
                    "hh_rank",
                    "hotness_rank",
                    "hotness_score",
                    "supply_score",
                    "demand_score",
                    "median_days_on_market",
                    "median_days_on_market_vs_us",
                    "median_days_on_market_month_on_month",
                    "hotness_rank_month_on_month",
                    "median_listing_price",
                    "median_listing_price_vs_us",
                    "median_listing_price_month_on_month",
                ],
            },
            {
                "name": "hobu.zipcode_market_hotness",
                "description": "Contains data related to a United States Zipcodes hotness score, supply score, demand score, days on market and listing prices.",
                "columns": [
                    "yyyymm",
                    "state_id",
                    "address",
                    "hh_rank",
                    "hotness_rank",
                    "hotness_score",
                    "supply_score",
                    "demand_score",
                    "median_days_on_market",
                    "median_days_on_market_vs_us",
                    "median_days_on_market_month_on_month",
                    "hotness_rank_month_on_month",
                    "median_listing_price",
                    "median_listing_price_vs_us",
                    "median_listing_price_month_on_month",
                ],
            },
        ],
        "glossary": [
            {
                "name": "yyyymm",
                "description": "Year and month of the data. data is aggregated by month.",
                "type": "INT, Eg: 202401, 202402 etc",
            },
            {
                "name": "state_id",
                "description": "2 character state code in uppercase",
                "type": "CHAR(2), Eg: NJ, CA etc",
            },
            {
                "name": "county_id",
                "description": "Name of the county in uppercase",
                "type": "TEXT, Eg: SOMERSET, CLARK, FULTON etc",
            },
            {
                "name": "county_name",
                "description": "Name of the county including the state",
                "type": "TEXT, Do not use this for any filtering instead use state_id and county_id fields",
            },
            {
                "name": "hh_rank",
                "description": "The specified zip code, county, or metro area’s rank by household count compared to other zip codes, counties and metro areas. A rank value of 1 is the highest by household count.",
                "type": "INT, Eg: 1, 2, 3 etc",
            },
            {
                "name": "hotness_rank",
                "description": "The specified zip code, county, or metro area’s Hotness rank, by Hotness score, compared to all other zip codes, counties and metro areas. A rank value of 1 is considered the hottest (highest Hotness score).",
                "type": "INT, Eg: 1, 2, 3 etc",
            },
            {
                "name": "hotness_score",
                "description": "The Hotness score is an equally-weighted composite metric of a geography’s supply score and demand score.",
                "type": "FLOAT, Ranges between 0.00 and 100.00",
            },
            {
                "name": "supply_score",
                "description": "The supply score is an index representing a zip code, county or metro’s median days on market ranking compared to other zip codes, counties, or metros.",
                "type": "FLOAT, Ranges between 0.00 and 100.00",
            },
            {
                "name": "demand_score",
                "description": "The demand score is an index representing a zip code, county or metro’s unique listing page viewers per property ranking compared to other zip codes, counties, or metros.",
                "type": "FLOAT, Ranges between 0.00 and 100.00",
            },
            {
                "name": "median_days_on_market",
                "description": "The median number of days property listings spend on the market within the specified geography during the specified month. Time spent on the market is defined as the time between the initial listing of a property and either its closing date or the date it is taken off the market.",
                "type": "FLOAT",
            },
            {
                "name": "median_days_on_market_vs_us",
                "description": "The median days on market in the specified geography divided by the median days on market for the US overall during the same month.",
                "type": "FLOAT",
            },
            {
                "name": "median_days_on_market_month_on_month",
                "description": "The change in days in the median days on market from the previous month.",
                "type": "FLOAT",
            },
            {
                "name": "hotness_rank_month_on_month",
                "description": "The specified zip code, county, or metro area’s Hotness rank in the previous month..",
                "type": "FLOAT, Ranges between 0.00 and 100.00",
            },
            {
                "name": "median_listing_price",
                "description": "The median listing price within the specified geography during the specified month.",
                "type": "FLOAT",
            },
            {
                "name": "median_listing_price_vs_us",
                "description": "The median listing price within the specified geography divided by the median listing price for the US overall during the same month.",
                "type": "FLOAT",
            },
            {
                "name": "median_listing_price_month_on_month",
                "description": "The percentage change in the median listing price from the previous month.",
                "type": "FLOAT",
            },
            {
                "name": "metro_name",
                "description": "The name of a US metro area in uppercase",
                "type": "TEXT, Eg: TULSA, WACO, TUCSON etc",
            },
            {
                "name": "address",
                "description": "The street address of the zip code",
                "type": "TEXT, Eg: 'tallmadge,oh', 'barberton, oh' etc",
            },
        ],
    }

    hobu_tools_state_dict = {"latest_yyyymm": "202407"}
