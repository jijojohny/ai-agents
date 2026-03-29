"""Example: Sales Outreach Agent."""
import os

from dotenv import load_dotenv

from main import SalesOutreachAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = SalesOutreachAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "Email to revive a stalled deal: they liked the demo but went dark 2 weeks.",
            verbose=True,
        )
    )
