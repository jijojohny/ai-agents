"""Release notes style helpers."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def release_notes_structure() -> str:
    """Recommended sections for user-facing release notes."""
    return (
        "Sections:\n"
        "- Headline / version\n"
        "- Highlights (3–5 user benefits)\n"
        "- New features\n"
        "- Improvements / fixes\n"
        "- Breaking changes + upgrade steps\n"
        "- Known issues / deprecations\n"
        "Write for customers first; keep engineer jargon secondary."
    )


@tool
def changelog_hygiene() -> str:
    """Hygiene rules when turning commits/PRs into notes."""
    return (
        "Group related commits; drop noise (typos, merge commits). "
        "Do not invent features not present in the input. "
        "Call out security fixes without disclosing exploit details. "
        "Flag ambiguous items for human confirmation."
    )


def get_release_notes_tools():
    return [release_notes_structure, changelog_hygiene]
