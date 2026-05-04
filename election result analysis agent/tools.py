"""Reference tools for responsible post-election analysis."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def official_data_citation_practices() -> str:
    """How to anchor claims after votes are reported."""
    return (
        "Good practice:\n"
        "- Tie each figure to **office + jurisdiction + reporting date/time** and **source** (e.g. state SOS, county canvass)\n"
        "- Distinguish **unofficial** vs **certified** results\n"
        "- Note batch types (Election Day vs mail vs provisional) when relevant\n"
        "Do not extrapolate demographic behavior without cited demographic data."
    )


@tool
def recount_and_certification_concepts() -> str:
    """High-level concepts (not legal advice; varies by jurisdiction)."""
    return (
        "Process concepts (varies by place):\n"
        "- Canvass / certification timelines\n"
        "- Recount triggers (margin thresholds) and risk-limiting audits where used\n"
        "- Provisional ballots and cure periods\n"
        "Always verify procedures with the relevant election official or counsel."
    )


@tool
def headline_vs_evidence_reminder() -> str:
    """Media literacy after results."""
    return (
        "Headline hygiene:\n"
        "- Landslide / mandate claims need defined baselines and full vote shares\n"
        "- Compare same **vote types** across years (apples-to-apples)\n"
        "- Correlation is not causation for turnout shifts\n"
        "Separate prediction from post-hoc description of certified counts."
    )


def get_election_result_tools():
    return [official_data_citation_practices, recount_and_certification_concepts, headline_vs_evidence_reminder]
