import os
from dotenv import load_dotenv
from main import PullRequestReviewAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = PullRequestReviewAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "Diff summary: new /api/export route streams CSV; uses sync DB call per row.",
            verbose=True,
        )
    )
