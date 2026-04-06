"""YouTube format reference tools."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def retention_pattern_hints() -> str:
    """Common patterns that support watch time (ethical use)."""
    return (
        "Retention patterns:\n"
        "- Open loop in first 5s; payoff before audience drops\n"
        "- Pattern breaks every ~45–90s (B-roll, question, example)\n"
        "- Clear chapters in description + verbal signposting\n"
        "- One strong CTA, not five\n"
        "Avoid misleading thumbnails/titles (policy + trust)."
    )


@tool
def hook_formula_examples() -> str:
    """Generic hook shapes (adapt to your niche)."""
    return (
        "Hook shapes:\n"
        "- Mistake: 'Most people get X wrong because…'\n"
        "- Result: 'I cut Y by 40% doing this one change…'\n"
        "- Contrarian: 'Stop doing X if you want Z…'\n"
        "- Story: 'Last Tuesday production went down because…'\n"
    )


def get_youtube_script_tools():
    return [retention_pattern_hints, hook_formula_examples]
