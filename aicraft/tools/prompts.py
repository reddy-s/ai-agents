from jinja2 import Environment, FileSystemLoader
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


class PromptConstructor:
    _instance = None

    @staticmethod
    def get_or_create_instance(template_folder: str):
        if PromptConstructor._instance is None:
            PromptConstructor._instance = PromptConstructor(template_folder)
        return PromptConstructor._instance

    def __init__(self, template_folder: str) -> None:
        self.file_loader = FileSystemLoader(template_folder)
        self.env = Environment(loader=self.file_loader)
        self.estate_agent_service_desk_template = self.env.get_template(
            "estate-agent-service-desk.tmpl"
        )
        self.preference_analysis_template = self.env.get_template(
            "preference-analysis.tmpl"
        )
        self.web_scraper_template = self.env.get_template("web-scraper.tmpl")
        self.data_analyst_template = self.env.get_template("data-analyst.tmpl")
        self.action_caller_template = self.env.get_template("action-caller.tmpl")

    def get_estate_agent_service_desk_prompt(self, data: dict) -> str:
        return self.estate_agent_service_desk_template.render(data)

    def get_preference_analysis_prompt(self, data: dict) -> str:
        return self.preference_analysis_template.render(data)

    def get_web_scraper_prompt(self, data: dict) -> str:
        return self.web_scraper_template.render(data)

    def get_data_analyst_prompt(self, data: dict) -> str:
        return self.data_analyst_template.render(data)

    def get_action_caller_prompt(self, data: dict) -> str:
        return self.action_caller_template.render(data)
