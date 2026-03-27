"""Optional structured schema for meeting notes output."""
from typing import List

from pydantic import BaseModel, Field


class MeetingNotesReply(BaseModel):
    summary: str = Field(description="Short summary of the meeting")
    decisions: List[str] = Field(default_factory=list, description="Key decisions made")
    action_items: List[str] = Field(default_factory=list, description="Actionable next steps")
    risks: List[str] = Field(default_factory=list, description="Risks or blockers identified")
