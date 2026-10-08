import os
from dotenv import load_dotenv
from main import LocalizationI18nAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = LocalizationI18nAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "Locales fr-FR, de-DE for settings page strings: Language, Time zone, Save. JSON please.",
            verbose=True,
        )
    )
