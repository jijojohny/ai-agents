"""RFC / design doc reference tools."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def rfc_template_sections() -> str:
    """Standard sections for an engineering RFC / design doc."""
    return (
        "RFC sections:\n"
        "- Title, authors, status, date\n"
        "- Context / problem statement\n"
        "- Goals and non-goals\n"
        "- Proposed design\n"
        "- Alternatives considered\n"
        "- Risks, rollout, rollback\n"
        "- Open questions / decision asks"
    )


@tool
def design_doc_review_focus() -> str:
    """What reviewers typically challenge."""
    return (
        "Reviewers look for:\n"
        "- Clear success metrics\n"
        "- Explicit tradeoffs vs alternatives\n"
        "- Failure modes and operability\n"
        "- Migration/compatibility story\n"
        "- Unstated assumptions called out"
    )


def get_rfc_design_doc_tools():
    return [rfc_template_sections, design_doc_review_focus]
