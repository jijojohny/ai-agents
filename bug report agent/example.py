"""
Example run for Bug Report Agent.
"""
import os

from dotenv import load_dotenv

from main import BugReportAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


def example_openai() -> None:
    agent = BugReportAgent(provider="openai", model_name="gpt-4o-mini")
    r = agent.chat(
        message=(
            "User says dark mode toggle flashes white screen on Android 14, "
            "Pixel 7, app v2.3.1. Only after cold start."
        ),
        verbose=True,
    )
    agent.print_result(r)


if __name__ == "__main__":
    example_openai()
