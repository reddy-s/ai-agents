import os
import streamlit as st

from copilot import Copilot


if __name__ == "__main__":
    if "HOBU_COPILOT_ASSETS" not in os.environ:
        raise Exception("Please set the environment variable HOBU_COPILOT_ASSETS")
    if "HOBU_COPILOT_PROMPT_TEMPLATES" not in os.environ:
        raise Exception(
            "Please set the environment variable HOBU_COPILOT_PROMPT_TEMPLATES"
        )
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise Exception(
            "Please set the environment variable GOOGLE_APPLICATION_CREDENTIALS"
        )
    if "OPENAI_API_KEY" not in os.environ:
        raise Exception("Please set the environment variable OPENAI_API_KEY")

    st.set_page_config(
        page_title="HoBu.ai | Co-Pilot",
        page_icon=f"{os.environ.get('HOBU_COPILOT_ASSETS')}/images/static/friends.png",
    )
    copilot = Copilot(context_history=5)
    copilot.run()
