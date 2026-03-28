"""
Helpers for X/Twitter post length and format patterns.
"""
from __future__ import annotations

from langchain_core.tools import tool

# Standard post limit for most accounts; Premium/longer posts are user-managed.
_DEFAULT_LIMIT = 280


@tool
def check_post_length(text: str, max_chars: int = _DEFAULT_LIMIT) -> str:
    """Check whether text fits a single post. Uses Python string length (good enough for ASCII/Latin).

    Args:
        text: Draft post body.
        max_chars: Character budget (default 280 for standard X posts).
    """
    t = text or ""
    limit = max(1, int(max_chars))
    n = len(t)
    if n <= limit:
        return f"OK: {n}/{limit} characters."
    return f"OVER: {n}/{limit} characters (trim by {n - limit})."


@tool
def list_viral_formats() -> str:
    """Return concise format patterns that often perform well on X (use ethically)."""
    return (
        "Format ideas:\n"
        "- Contrarian one-liner: flip a common belief with one proof hint\n"
        "- Specific story: one scene + lesson + takeaway\n"
        "- Numbered list: 3–5 tight bullets, last line CTA\n"
        "- Question hook: sharp question + your answer in next line\n"
        "- Before/after: old way vs new way + why it matters\n"
        "- Thread opener: line 1 promise + line 2 preview of payoff"
    )


def get_twitter_viral_tools():
    return [check_post_length, list_viral_formats]
