"""a11y checklist reference tools."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def wcag_focus_areas() -> str:
    """High-level WCAG themes (informal)."""
    return (
        "Focus areas:\n"
        "- Perceivable: text alternatives, contrast, resize/reflow\n"
        "- Operable: keyboard, focus order, no seizure triggers\n"
        "- Understandable: labels, errors, consistent nav\n"
        "- Robust: valid markup, name/role/value for custom controls\n"
        "Map findings to WCAG success criteria with an auditor when needed."
    )


@tool
def keyboard_nav_prompts() -> str:
    """Questions for keyboard-only paths."""
    return (
        "Keyboard checks:\n"
        "- All interactive elements focusable and visible focus ring?\n"
        "- Traps in modals/menus Esc to close?\n"
        "- Skip link to main content?\n"
        "- Tab order matches reading order?\n"
    )


def get_a11y_review_tools():
    return [wcag_focus_areas, keyboard_nav_prompts]
