import os
from dotenv import load_dotenv
from main import JobDescriptionWriterAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = JobDescriptionWriterAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "Junior data analyst JD for a nonprofit. Remote US. Must: SQL, sheets. Nice: Looker. JSON please.",
            verbose=True,
        )
    )
