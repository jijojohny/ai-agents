"""SEO brief helper tools (no live SERP scraping)."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def seo_brief_structure() -> str:
    """Recommended fields for an SEO content brief."""
    return (
        "SEO brief checklist:\n"
        "- Primary keyword + search intent\n"
        "- Secondary / related terms (not stuffed)\n"
        "- Title options + meta description length target (~150–160 chars)\n"
        "- H2 outline covering depth competitors typically need\n"
        "- FAQs / People Also Ask style questions\n"
        "- Internal link opportunities (conceptual)\n"
        "- E-E-A-T / YMYL caveats when relevant"
    )


@tool
def seo_quality_red_flags() -> str:
    """Common SEO content mistakes."""
    return (
        "Avoid:\n"
        "- Keyword stuffing and thin AI filler\n"
        "- Promising rankings without crawl/index data\n"
        "- Inventing competitor rankings or search volume numbers\n"
        "- Ignoring intent mismatch (informational vs transactional)\n"
        "Mark unknowns; user should verify with Search Console / keyword tools."
    )


def get_seo_content_brief_tools():
    return [seo_brief_structure, seo_quality_red_flags]
