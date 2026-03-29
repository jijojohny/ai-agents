"""Lightweight helpers for outbound sales copy."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def classify_outreach_stage(brief: str) -> str:
    """Map a short brief to a simple funnel stage for tone and length."""
    text = (brief or "").lower()
    if any(k in text for k in ("cold", "never met", "first touch")):
        return "cold — very short, one insight, soft CTA"
    if any(k in text for k in ("demo", "trial", "pricing", "proposal")):
        return "late — direct CTA, recap value, next step with time options"
    if any(k in text for k in ("follow up", "no reply", "bump")):
        return "nurture — new angle, bump earlier value, low guilt"
    return "mid — clarify fit, ask one qualifying question"


@tool
def outreach_length_guidelines(channel: str) -> str:
    """Rough length hints by channel."""
    ch = (channel or "email").strip().lower()
    if ch in ("linkedin", "li", "dm"):
        return "LinkedIn/DM: ~50–120 words often works; first line is the hook; avoid walls of text."
    return "Email: ~100–200 words for first touch; subject <60 chars; one CTA only."


def get_sales_outreach_tools():
    return [classify_outreach_stage, outreach_length_guidelines]
