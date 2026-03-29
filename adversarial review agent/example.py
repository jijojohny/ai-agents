"""Example: deep adversarial review pipeline."""
import os

from dotenv import load_dotenv

from main import AdversarialReviewAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


if __name__ == "__main__":
    agent = AdversarialReviewAgent(provider="openai", model_name="gpt-4o-mini")
    r = agent.run_deep_review(
        proposal="Migrate auth to passwordless only; remove password login in one release.",
        extra_context="B2B SaaS, 10k MAU, regulated industry.",
        verbose=True,
    )
    agent.print_deep_result(r)
