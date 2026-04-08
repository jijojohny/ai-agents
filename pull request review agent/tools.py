"""Code review tone and severity helpers."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def review_comment_tone_guide() -> str:
    """Constructive code review phrasing."""
    return (
        "Tone:\n"
        "- Ask questions instead of accusing: 'Could this race if X?'\n"
        "- Suggest alternatives: 'Consider Y because Z.'\n"
        "- Separate must-fix vs nit; praise specific good choices.\n"
        "- Assume good intent; avoid sarcasm.\n"
        "Reference project standards when known."
    )


@tool
def pr_severity_rubric() -> str:
    """Rough severity labels for review threads."""
    return (
        "Severity:\n"
        "- blocking: correctness, security, data loss, broken build\n"
        "- important: bugs, perf regressions, missing tests for risky paths\n"
        "- suggestion: readability, naming, small refactors\n"
        "- praise: highlight what to repeat\n"
    )


def get_pr_review_tools():
    return [review_comment_tone_guide, pr_severity_rubric]
