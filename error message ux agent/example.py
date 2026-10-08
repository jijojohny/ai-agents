import os
from dotenv import load_dotenv
from main import ErrorMessageUxAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = ErrorMessageUxAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "403 Forbidden uploading avatar over 5MB. Friendly copy + recovery + JSON.",
            verbose=True,
        )
    )
