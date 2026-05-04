"""
Educational tools for election literacy — no live poll data (user must supply numbers).
"""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def polling_uncertainty_reminder() -> str:
    """Why headline margins are not guarantees."""
    return (
        "Polling literacy:\n"
        "- Margin of error applies to **each** number; gaps smaller than ~2×MOE are hard to distinguish\n"
        "- Likely-voter models, language, and weighting change results (house effects)\n"
        "- Polls are snapshots; events, turnout, and undecideds can move outcomes\n"
        "Never treat a single poll as truth; prefer aggregates with transparent methods."
    )


@tool
def us_electoral_college_reminder() -> str:
    """US presidential context only — high level."""
    return (
        "US Electoral College (high level):\n"
        "- Most states are winner-take-all; Maine/Nebraska split by congressional district rules\n"
        "- 270 electoral votes wins; national popular vote ≠ EC outcome possible\n"
        "- Certification, recounts, and legal processes follow state/federal law\n"
        "This is civic education, not a projection engine."
    )


@tool
def forecast_ethics_checklist() -> str:
    """Responsible communication about election estimates."""
    return (
        "Ethics checklist:\n"
        "- Do not claim certainty or insider knowledge\n"
        "- Label scenarios vs. evidence-based ranges; cite sources for numbers\n"
        "- Avoid content that could suppress turnout or incite harassment\n"
        "- Respect platform and local laws on political advertising and disclosures\n"
        "Encourage voting based on non-deceptive information from trusted authorities."
    )


def get_election_tools():
    return [polling_uncertainty_reminder, us_electoral_college_reminder, forecast_ethics_checklist]
