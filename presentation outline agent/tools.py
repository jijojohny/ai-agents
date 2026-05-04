from langchain_core.tools import tool


@tool
def pyramid_principle_deck() -> str:
    """McKinsey-style slide thinking (lightweight)."""
    return (
        "Lead each slide with the answer (what you want them to remember).\n"
        "Support with 2–4 bullets max; evidence on next slide if heavy.\n"
        "One message per slide; remove duplicate titles across deck."
    )


@tool
def slide_density_rule_of_thumb() -> str:
    """Timing vs slide count."""
    return (
        "~1–2 minutes per slide for deep talks; faster for lightning.\n"
        "Budget 10–15% of time for Q&A unless format forbids.\n"
        "Put appendix slides after a hard stop slide if needed."
    )


def get_presentation_tools():
    return [pyramid_principle_deck, slide_density_rule_of_thumb]
