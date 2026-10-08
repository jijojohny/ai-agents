"""Onboarding planning reference tools."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def onboarding_structure() -> str:
    """Recommended structure for an onboarding guide."""
    return (
        "Onboarding structure:\n"
        "- Goals / success criteria for 30-60-90\n"
        "- Day 1 access, intros, and setup\n"
        "- Week 1 core workflows and shadowing\n"
        "- Month 1 ownership and feedback checkpoints\n"
        "- Role owners (manager, buddy, IT, HR)\n"
        "- Checklist of accounts, docs, and first deliverable"
    )


@tool
def onboarding_anti_patterns() -> str:
    """Common onboarding failure modes."""
    return (
        "Avoid:\n"
        "- Dumping docs without a first win\n"
        "- Unclear owners for access requests\n"
        "- Inventing company policies or legal requirements\n"
        "- Overloading day 1 with meetings only\n"
        "Prefer paced checklists with explicit owners."
    )


def get_onboarding_guide_tools():
    return [onboarding_structure, onboarding_anti_patterns]
