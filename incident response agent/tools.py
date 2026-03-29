"""Reference playbooks for incident handling."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def incident_severity_cheatsheet() -> str:
    """Rough severity framing (adapt to your org's definitions)."""
    return (
        "Severity hints (typical):\n"
        "- sev1: full outage / data loss / active exploit / irreversible harm\n"
        "- sev2: major degradation, large % users, no workaround\n"
        "- sev3: partial impact or workaround exists\n"
        "- sev4: minor, cosmetic, internal-only\n"
        "Always align with your on-call policy and executive comms rules."
    )


@tool
def blameless_postmortem_outline() -> str:
    """Sections for a blameless post-incident review."""
    return (
        "Postmortem outline:\n"
        "- Summary & impact (users, revenue, SLA)\n"
        "- Timeline (detection → mitigation → resolution)\n"
        "- Root cause & contributing factors\n"
        "- What went well\n"
        "- What went poorly\n"
        "- Action items (owner, due date)\n"
        "- Lessons learned"
    )


def get_incident_tools():
    return [incident_severity_cheatsheet, blameless_postmortem_outline]
