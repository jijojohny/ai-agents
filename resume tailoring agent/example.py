import os
from dotenv import load_dotenv
from main import ResumeTailoringAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = ResumeTailoringAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "Job: Staff SRE. My experience: on-call rotations, Terraform modules, incident postmortems.",
            verbose=True,
        )
    )
