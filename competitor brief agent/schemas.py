"""Competitor brief structured reply."""
from typing import List, Optional

from pydantic import BaseModel, Field


class CompetitorEntry(BaseModel):
    name: str
    positioning: str = ""
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    pricing_notes: Optional[str] = None
    sources_needed: List[str] = Field(
        default_factory=list,
        description="What the user should verify with public sources",
    )


class CompetitorBriefReply(BaseModel):
    market_frame: str = Field(description="Category / ICP framing")
    competitors: List[CompetitorEntry] = Field(default_factory=list)
    differentiation_angles: List[str] = Field(default_factory=list)
    risks_assumptions: List[str] = Field(default_factory=list)
    next_research_steps: List[str] = Field(default_factory=list)
