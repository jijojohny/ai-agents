import os
from dotenv import load_dotenv
from main import DockerComposeAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
if __name__ == "__main__":
    a = DockerComposeAgent("openai", "gpt-4o-mini")
    a.print_result(
        a.chat(
            "Three services: worker consuming Redis queue, API container, Postgres — named volumes for PG data.",
            verbose=True,
        )
    )
