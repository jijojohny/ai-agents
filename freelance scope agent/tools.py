from langchain_core.tools import tool


@tool
def sow_structure_reminder() -> str:
    """Standard freelance scope sections (non-exhaustive)."""
    return (
        "Typical SOW sections: background, objectives, deliverables, timeline,\n"
        "dependencies (client provides), acceptance criteria, change process,\n"
        "IP / confidentiality pointers (lawyer for binding terms).\n"
        "Never invent rates or legal commitments."
    )


@tool
def milestone_acceptance_hint() -> str:
    """How to phrase milestones usefully."""
    return (
        "Each milestone: verb + artifact + objective acceptance signal.\n"
        "Example: 'Draft wireframes delivered as Figma link; client feedback round within 5 biz days.'\n"
        "Avoid vague 'phase complete' without observable output."
    )


def get_freelance_scope_tools():
    return [sow_structure_reminder, milestone_acceptance_hint]
