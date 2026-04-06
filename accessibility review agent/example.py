import os
from dotenv import load_dotenv
from main import AccessibilityReviewAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = AccessibilityReviewAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "Signup form: placeholders instead of labels, password rules only in tooltip.",
            verbose=True,
        )
    )
