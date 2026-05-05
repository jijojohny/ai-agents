import os
from dotenv import load_dotenv
from main import FreelanceScopeAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
if __name__ == "__main__":
    a = FreelanceScopeAgent("openai", "gpt-4o-mini")
    a.print_result(
        a.chat(
            "Retainer: up to 10h/month technical writing for API docs; respond within 48h on weekdays.",
            verbose=True,
        )
    )
