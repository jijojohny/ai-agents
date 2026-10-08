import os
from dotenv import load_dotenv
from main import DependencyUpgradeAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = DependencyUpgradeAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "Go module: upgrade gin and jwt libs one minor each. Order + rollback + JSON.",
            verbose=True,
        )
    )
