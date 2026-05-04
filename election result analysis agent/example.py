import os
from dotenv import load_dotenv
from main import ElectionResultAnalysisAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = ElectionResultAnalysisAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_pipeline(
        agent.run_pipeline(
            results_and_context=(
                "Local measure L. Unofficial 2026-03-03: Yes 12,400 (54%), No 10,500 (46%). "
                "Source: county clerk website; 100% precincts; not yet certified."
            ),
            extra_notes="Compare to prior cycle not available.",
            verbose=True,
        )
    )
