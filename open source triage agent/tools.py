from langchain_core.tools import tool


@tool
def issue_reply_etiquette() -> str:
    """Tone for public issue threads."""
    return (
        "Thank the reporter; ask minimal follow-ups (version, OS, repro).\n"
        "Link to docs if usage question; convert to discussion if policy allows.\n"
        "Set expectations on maintainer bandwidth; invite PRs when appropriate."
    )


@tool
def duplicate_and_stale_issue_hints() -> str:
    """Triage hygiene."""
    return (
        "Search existing issues/PRs for duplicates.\n"
        "If needs-info: label + auto-close policy if your project uses one.\n"
        "Lock heated threads per code of conduct."
    )


def get_oss_triage_tools():
    return [issue_reply_etiquette, duplicate_and_stale_issue_hints]
