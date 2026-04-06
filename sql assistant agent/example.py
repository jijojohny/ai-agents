import os
from dotenv import load_dotenv
from main import SQLAssistantAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = SQLAssistantAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "BigQuery: SELECT daily signups from table events where type='signup', date column ts.",
            verbose=True,
        )
    )
