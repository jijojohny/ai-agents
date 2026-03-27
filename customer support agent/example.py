"""
Examples: Customer Support Agent.
"""
import os

from dotenv import load_dotenv

from main import CustomerSupportAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


def example_openai() -> None:
    agent = CustomerSupportAgent(provider="openai", model_name="gpt-4o-mini")
    r = agent.chat(
        message="Customer says: 'My package is 8 days late and tracking never updates.'",
        verbose=True,
    )
    agent.print_result(r)


if __name__ == "__main__":
    example_openai()
