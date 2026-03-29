"""Example: Study Coach Agent."""
import os

from dotenv import load_dotenv

from main import StudyCoachAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = StudyCoachAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "Here are my notes:\n- Kosaraju finds SCCs using two passes...\n"
            "Turn into flashcards + 3 practice questions.",
            verbose=True,
        )
    )
