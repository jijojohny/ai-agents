"""Competitor analysis reference tools (no live web scrape)."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def competitor_brief_framework() -> str:
    """Dimensions to cover in a competitor brief."""
    return (
        "Cover:\n"
        "- Category definition and ICP overlap\n"
        "- Positioning / messaging themes\n"
        "- Product surface (features that matter to buyers)\n"
        "- Pricing model (only if user-provided or clearly labeled as unknown)\n"
        "- Go-to-market motions\n"
        "- Differentiation opportunities for the user's product\n"
        "- Evidence gaps and verification steps"
    )


@tool
def competitor_analysis_ethics() -> str:
    """Guardrails for competitive analysis."""
    return (
        "Do not invent market shares, ARR, or confidential pricing. "
        "Label speculation. Prefer user-pasted notes and cite what must be checked "
        "on public sites. Avoid illegal or unethical collection advice."
    )


def get_competitor_brief_tools():
    return [competitor_brief_framework, competitor_analysis_ethics]
