"""Dependency upgrade planning reference tools."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def upgrade_playbook() -> str:
    """Safe dependency upgrade sequencing."""
    return (
        "Upgrade playbook:\n"
        "- Read changelogs / migration guides for major bumps\n"
        "- Upgrade one risky dependency (or tightly coupled set) at a time\n"
        "- Run unit/integration/e2e smoke after each step\n"
        "- Pin or lockfile-commit for reproducibility\n"
        "- Plan rollback (previous lockfile / release)\n"
        "- Prefer security patches promptly; defer cosmetic majors if blocked"
    )


@tool
def upgrade_red_flags() -> str:
    """Signals that an upgrade needs extra caution."""
    return (
        "Red flags:\n"
        "- Major version jumps across frameworks\n"
        "- Native / binary addons and ABI changes\n"
        "- Auth, crypto, or HTTP client libraries\n"
        "- Inventing CVE details—ask user for advisory text\n"
        "- Skipping tests because 'it compiled'"
    )


def get_dependency_upgrade_tools():
    return [upgrade_playbook, upgrade_red_flags]
