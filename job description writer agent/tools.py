"""Reference tools for inclusive, clear job descriptions."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def jd_structure_checklist() -> str:
    """Recommended sections for a complete job description."""
    return (
        "Job description sections:\n"
        "1. Title + team/location/work model (remote/hybrid/onsite)\n"
        "2. Mission / role summary (2–4 sentences)\n"
        "3. Responsibilities (bullets; outcome-oriented)\n"
        "4. Must-have requirements (skills, experience bands—avoid inflated years)\n"
        "5. Nice-to-haves (clearly labeled)\n"
        "6. Benefits / process notes (only if provided by user)\n"
        "7. Equal opportunity / inclusive language cues"
    )


@tool
def inclusive_language_red_flags() -> str:
    """Phrases that often signal bias or unnecessary barriers."""
    return (
        "Watch for:\n"
        "- Gendered language (ninja, rockstar, guys)\n"
        "- Unjustified degree requirements\n"
        "- 'Native speaker' when fluency is enough\n"
        "- Vague 'culture fit' without behaviors\n"
        "- Inflated year requirements for junior tools\n"
        "Prefer concrete skills and examples of work product."
    )


def get_job_description_tools():
    return [jd_structure_checklist, inclusive_language_red_flags]
