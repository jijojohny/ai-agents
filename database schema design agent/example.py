import os
from dotenv import load_dotenv
from main import DatabaseSchemaDesignAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = DatabaseSchemaDesignAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "SQLite-friendly schema for personal expense tracker: accounts, categories, transactions. JSON.",
            verbose=True,
        )
    )
