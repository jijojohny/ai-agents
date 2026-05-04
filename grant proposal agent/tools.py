from langchain_core.tools import tool


@tool
def rfp_alignment_checklist() -> str:
    """Common grant section alignment."""
    return (
        "Checklist:\n"
        "- Eligibility and page limits / font rules\n"
        "- Evaluation criteria mirrored in headings\n"
        "- SMART outcomes tied to funder priorities\n"
        "- Letters of support / data management / IRB if human subjects\n"
        "Paste the funder’s required outline if available."
    )


@tool
def budget_red_flags_reminder() -> str:
    """Ethical budgeting reminders."""
    return (
        "Do not fabricate salaries or institutional rates.\n"
        "Indirect / F&A must match institutional policy and funder rules.\n"
        "Cost share only if allowed and real.\n"
        "Consult institutional grants office for final numbers."
    )


def get_grant_tools():
    return [rfp_alignment_checklist, budget_red_flags_reminder]
