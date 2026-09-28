import os
from dotenv import load_dotenv
from main import ReleaseNotesAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = ReleaseNotesAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "0.9.1: dependency bump only + security patch for auth cookie. Keep vague on exploit. JSON.",
            verbose=True,
        )
    )
