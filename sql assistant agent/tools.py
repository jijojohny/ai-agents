"""SQL safety and style reference tools."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def read_only_sql_policy() -> str:
    """Policy reminder for generated SQL."""
    return (
        "Read-only policy for suggestions:\n"
        "- Prefer SELECT / WITH only; no INSERT/UPDATE/DELETE/DROP/ALTER/TRUNCATE.\n"
        "- Use parameterized queries in apps; never concatenate raw user input into SQL strings.\n"
        "- Add LIMIT on exploratory queries when appropriate.\n"
        "- Qualify table names/schemas; avoid SELECT * in production paths."
    )


@tool
def sql_injection_red_flags() -> str:
    """Patterns to avoid when users paste untrusted input."""
    return (
        "Red flags:\n"
        "- String-building from end-user text without binding\n"
        "- Dynamic ORDER BY / column names from user input\n"
        "- Stacked statements (; DROP …)\n"
        "Use bound parameters and allow-lists for identifiers."
    )


def get_sql_assistant_tools():
    return [read_only_sql_policy, sql_injection_red_flags]
