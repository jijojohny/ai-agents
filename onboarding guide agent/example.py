import os
from dotenv import load_dotenv
from main import OnboardingGuideAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = OnboardingGuideAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "Product manager onboarding at a startup. Remote-first. Day1/Week1/Month1 + JSON.",
            verbose=True,
        )
    )
