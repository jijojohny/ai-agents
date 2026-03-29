"""
Reference rubrics for advanced review (non-LLM helpers).
"""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def risk_review_dimensions() -> str:
    """Dimensions to stress-test a plan or product decision."""
    return (
        "Review dimensions:\n"
        "- Correctness & edge cases\n"
        "- Security & abuse (fraud, spam, prompt injection if AI)\n"
        "- Privacy & compliance (data minimization, consent)\n"
        "- Reliability & ops (SLOs, rollbacks, incident playbooks)\n"
        "- Cost & scalability\n"
        "- UX harm & accessibility\n"
        "- Reputational & legal risk\n"
        "- Strategic fit & opportunity cost"
    )


@tool
def assumption_spotting_prompt() -> str:
    """Short checklist to surface hidden assumptions."""
    return (
        "Assumption audit:\n"
        "- What must be true about users, market, or infra?\n"
        "- What are we optimizing for vs de-prioritizing?\n"
        "- What evidence would falsify this plan?\n"
        "- What happens under 10x load or 10x abuse?\n"
    )


def get_adversarial_tools():
    return [risk_review_dimensions, assumption_spotting_prompt]
