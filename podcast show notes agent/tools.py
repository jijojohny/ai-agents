from langchain_core.tools import tool


@tool
def chapter_marker_convention() -> str:
    """Common chapter line format for editors."""
    return "Use [HH:MM:SS] Topic — one line per chapter; align with your DAW or hosting export timestamps."


@tool
def podcast_description_seo_tips() -> str:
    """Short tips for directory listings."""
    return (
        "First 1–2 sentences: who it's for + promise.\n"
        "Include guest name/role if interview.\n"
        "3–8 relevant keywords naturally; avoid keyword stuffing.\n"
        "Timestamps in description boost UX on some platforms."
    )


def get_podcast_tools():
    return [chapter_marker_convention, podcast_description_seo_tips]
