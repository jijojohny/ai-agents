import os
from dotenv import load_dotenv
from main import ApiDesignAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = ApiDesignAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "CRUD for customer saved filters + share link with read-only token.",
            verbose=True,
        )
    )
