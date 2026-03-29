"""Example: full incident response pipeline."""
import os

from dotenv import load_dotenv

from main import IncidentResponseAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


if __name__ == "__main__":
    agent = IncidentResponseAgent(provider="openai", model_name="gpt-4o-mini")
    r = agent.run_full_response(
        incident_description=(
            "Search cluster yellow; p95 latency 3x normal. Recent index rebuild job running."
        ),
        extra_context="Single region; business hours; ~50k QPS peak.",
        verbose=True,
    )
    agent.print_full_result(r)
