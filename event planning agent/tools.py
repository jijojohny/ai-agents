from langchain_core.tools import tool


@tool
def run_of_show_format() -> str:
    """Run-of-show line pattern."""
    return (
        "Each line: time or relative offset — owner — activity — inputs/outputs.\n"
        "Example: '09:55–10:00 — MC — housekeeping + Wi-Fi slide — slide deck v3'.\n"
        "Buffer 10–15% for hybrid Q&A and tech glitches."
    )


@tool
def hybrid_event_reminders() -> str:
    """Hybrid / virtual logistics touchpoints."""
    return (
        "For hybrid: stage platform checks, moderator chat monitoring, backup dial-in,\n"
        "recording consent and retention note, captioning access link."
    )


def get_event_planning_tools():
    return [run_of_show_format, hybrid_event_reminders]
