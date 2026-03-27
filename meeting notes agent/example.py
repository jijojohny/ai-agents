"""
Example run for Meeting Notes Agent.
"""
import os

from dotenv import load_dotenv

from main import MeetingNotesAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


def example_openai() -> None:
    agent = MeetingNotesAgent(provider="openai", model_name="gpt-4o-mini")
    raw_notes = """
    Weekly sync:
    - Decision: move launch to next Thursday.
    - Action: Alex to update release checklist by Tuesday.
    - API integration is blocked on vendor response.
    - QA found 2 critical bugs in onboarding.
    """
    r = agent.chat(message=f"Summarize these notes and produce actions:\n{raw_notes}", verbose=True)
    agent.print_result(r)


if __name__ == "__main__":
    example_openai()
