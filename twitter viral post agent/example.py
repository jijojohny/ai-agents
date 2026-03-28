"""
Example run for Twitter / X Viral Post Agent.
"""
import os

from dotenv import load_dotenv

from main import TwitterViralPostAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


def example_openai() -> None:
    agent = TwitterViralPostAgent(provider="openai", model_name="gpt-4o-mini", temperature=0.8)
    r = agent.chat(
        message=(
            "Niche: indie hackers. Topic: shipping weekly in public. "
            "Give a punchy post under 280 chars plus 2 alternate hooks."
        ),
        verbose=True,
    )
    agent.print_result(r)


if __name__ == "__main__":
    example_openai()
