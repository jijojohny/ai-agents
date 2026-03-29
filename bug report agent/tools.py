"""
Heuristics for bug severity and a repro template.
"""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def classify_severity_hint(description: str) -> str:
    """Rough severity hint from keywords (not a substitute for triage)."""
    text = (description or "").lower()
    if any(k in text for k in ("data loss", "security", "breach", "unauthorized", "wallet", "payment")):
        return "hint: critical_or_high — verify security/data impact"
    if any(k in text for k in ("outage", "down", "500", "cannot login", "blocked", "production")):
        return "hint: high — widespread or blocking"
    if any(k in text for k in ("crash", "error", "broken", "regression")):
        return "hint: medium — functional break"
    if any(k in text for k in ("typo", "cosmetic", "alignment", "color")):
        return "hint: low — mostly visual"
    return "hint: medium_or_unknown — need repro and scope"


@tool
def repro_template() -> str:
    """Return a markdown skeleton for steps to reproduce."""
    return (
        "## Steps to reproduce\n"
        "1. \n"
        "2. \n"
        "3. \n\n"
        "## Expected\n"
        "\n\n"
        "## Actual\n"
        "\n\n"
        "## Environment\n"
        "- App version / commit:\n"
        "- OS / browser / device:\n"
        "- Account type (if relevant):\n"
    )


def get_bug_report_tools():
    return [classify_severity_hint, repro_template]
