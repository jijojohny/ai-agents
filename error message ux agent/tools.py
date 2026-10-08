"""Error copy UX reference tools."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def error_copy_principles() -> str:
    """Principles for clear user-facing error messages."""
    return (
        "Error copy principles:\n"
        "- Say what happened in plain language\n"
        "- Say what the user can do next (primary recovery)\n"
        "- Avoid blame ('you failed'); prefer system ownership\n"
        "- Keep technical details for logs/support, not the modal\n"
        "- Match severity: info vs blocking error"
    )


@tool
def error_security_hygiene() -> str:
    """What not to put in user-visible errors."""
    return (
        "Do not expose:\n"
        "- Stack traces, SQL, file paths, secrets, tokens\n"
        "- Internal hostnames or raw vendor error dumps\n"
        "- Enumeration-friendly auth details when avoidable\n"
        "Offer a support/reference id instead when useful."
    )


def get_error_message_ux_tools():
    return [error_copy_principles, error_security_hygiene]
