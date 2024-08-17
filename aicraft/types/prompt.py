from enum import Enum


class PromptType(Enum):
    ESTATE_AGENT_SERVICE_DESK = "get_estate_agent_service_desk_prompt"
    PREFERENCE_ANALYSIS = "get_preference_analysis_prompt"
    WEB_SCRAPING = "get_web_scraper_prompt"
    DATA_ANALYST = "get_data_analyst_prompt"
    ACTION_CALLER = "get_action_caller_prompt"
