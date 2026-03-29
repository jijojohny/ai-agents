"""Structured outreach package."""
from typing import List

from pydantic import BaseModel, Field


class OutreachReply(BaseModel):
    channel: str = Field(description="email, linkedin, or other")
    subject_or_hook: str = Field(description="Subject line or first-line hook")
    body: str = Field(description="Main message body")
    call_to_action: str = Field(description="Clear single CTA")
    follow_up_sequence: List[str] = Field(
        default_factory=list,
        description="Short follow-up 2–3 touch ideas with timing hints",
    )
    research_questions: List[str] = Field(
        default_factory=list,
        description="Facts to verify before sending",
    )
