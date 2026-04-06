"""Newsletter structure helpers."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def newsletter_skeleton() -> str:
    """Classic newsletter section order."""
    return (
        "Skeleton:\n"
        "1. Hook / personal note (1–3 sentences)\n"
        "2. Main story or insight\n"
        "3. Secondary link or tip\n"
        "4. CTA (one ask)\n"
        "5. P.S. optional\n"
        "Keep scannable: short paragraphs, bullets."
    )


@tool
def subject_line_checklist() -> str:
    """Subject line hygiene."""
    return (
        "Subject lines:\n"
        "- Specific > vague; avoid ALL CAPS spam cues\n"
        "- 40–60 chars often preview well\n"
        "- Match body promise (no bait-and-switch)\n"
        "- Test plain vs curiosity (brand-dependent)"
    )


def get_newsletter_tools():
    return [newsletter_skeleton, subject_line_checklist]
