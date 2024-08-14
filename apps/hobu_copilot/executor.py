import os
from streamlit.delta_generator import DeltaGenerator
from aicraft.types import CodingAgentResponse, Roles
from agents import WebScraper
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Executor:
    def __init__(self):
        self.web_scraper = WebScraper(os.environ.get("HOBU_COPILOT_PROMPT_TEMPLATES"))

    @staticmethod
    def executeCode(code: str, return_var: str) -> str | None:
        logger.info(f"Executing code:============== \n{code}")
        local_vars = {}
        exec(code, {}, local_vars)
        file_location = local_vars.get(return_var)
        if file_location is not None:
            os.path.exists(file_location)
            return file_location
        else:
            return None

    def scrape_the_web_page(
        self, url: str, max_retries: int = 3
    ) -> tuple[str, str | None, list[dict]]:
        start = time.time()
        file_location = None
        code_conv = [
            {
                "role": Roles.user.value,
                "content": f"write python code to scrape HTML from {url}, store it into a .html file and return the file location for further processing",
            }
        ]

        for i in range(max_retries):
            code = self.web_scraper.analyse(
                code_conv,
                state={},
            )

            if type(code.content) is CodingAgentResponse:
                code_conv.append(
                    {
                        "role": Roles.assistant.value,
                        "content": code.content.executableCode,
                    }
                )
                try:
                    file_location = Executor.executeCode(
                        code.content.executableCode, "file_location"
                    )
                    break
                except Exception as e:
                    logger.info(
                        f"Got the following error executing the code: {e} and hence trying again."
                    )
                    code_conv.append(
                        {
                            "role": Roles.user.value,
                            "content": f"Got the following error executing the code: {e}. try again.",
                        }
                    )
        elapsed = f"{round(time.time() - start, 1)}s"

        return elapsed, file_location, code_conv
