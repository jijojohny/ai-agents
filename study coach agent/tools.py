"""Study-method helpers."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def active_recall_prompts() -> str:
    """Short list of generic active-recall prompts to apply to any topic."""
    return (
        "Active recall:\n"
        "- Explain the idea in 2 sentences without looking.\n"
        "- List 3 edge cases or exceptions.\n"
        "- Teach it: what would confuse a beginner?\n"
        "- Draw a diagram or mental model in words."
    )


@tool
def pomodoro_study_block() -> str:
    """Simple time-box suggestion (not medical advice)."""
    return "Try 25 min focus / 5 min break × 3, then a longer break. Adjust to your stamina."


def get_study_coach_tools():
    return [active_recall_prompts, pomodoro_study_block]
