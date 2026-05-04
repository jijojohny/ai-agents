import os
from dotenv import load_dotenv
from main import ElectionPredictionAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = ElectionPredictionAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "Scenario only: if turnout among group A rises 5 pts vs 2020 baseline, what kinds of "
            "evidence would we need before saying anything quantitative? No invented polls.",
            verbose=True,
        )
    )
