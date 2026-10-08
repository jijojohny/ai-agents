import os
from dotenv import load_dotenv
from main import RfcDesignDocAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = RfcDesignDocAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "RFC: replace nightly full ETL with incremental CDC into warehouse. Goals/non-goals + JSON.",
            verbose=True,
        )
    )
