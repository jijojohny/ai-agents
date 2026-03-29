"""Example: Travel Planner Agent."""
import os

from dotenv import load_dotenv

from main import TravelPlannerAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = TravelPlannerAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "Weekend in Chicago: kid-friendly, low budget, early May.",
            verbose=True,
        )
    )
