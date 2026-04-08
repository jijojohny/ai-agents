"""Resume writing reference tools."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def bullet_star_reminder() -> str:
    """Action + context + result pattern for bullets."""
    return (
        "Strong bullets:\n"
        "- Lead with strong verb + scope (team, product, scale)\n"
        "- Quantify when true: latency %, revenue, users, error rate\n"
        "- One idea per bullet; avoid jargon soup\n"
        "Use [METRIC TBD] if the user has not provided a number—never invent metrics."
    )


@tool
def ats_readability_tips() -> str:
    """Simple ATS-friendly habits (not a guarantee of scoring)."""
    return (
        "Readability:\n"
        "- Mirror **honest** keywords from the JD in skills/experience\n"
        "- Standard section titles: Experience, Education, Skills\n"
        "- Avoid tables/text boxes that break parsing in some systems\n"
        "ATS behavior varies by employer—this is general guidance only."
    )


def get_resume_tailor_tools():
    return [bullet_star_reminder, ats_readability_tips]
