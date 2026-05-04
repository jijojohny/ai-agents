"""Structured election scenario analysis (not a certified forecast)."""
from typing import List, Optional

from pydantic import BaseModel, Field


class ElectionScenarioReply(BaseModel):
    jurisdiction: str = Field(default="", description="Country/region/office, e.g. US general 2024")
    question_framing: str = Field(description="What is being estimated and what is out of scope")
    assumptions: List[str] = Field(default_factory=list, description="Explicit assumptions")
    uncertainty_drivers: List[str] = Field(
        default_factory=list,
        description="Turnout, polling error, late shifts, etc.",
    )
    scenario_notes: List[str] = Field(
        default_factory=list,
        description="Qualitative scenarios (e.g. if polls understate X)—no false precision",
    )
    data_sources_user_provided: Optional[str] = Field(
        default=None,
        description="Reminder: cite polls the user pasted; do not invent numbers",
    )
    disclaimer: str = Field(
        default="Not a forecast service. LLMs cannot know future votes; verify with official election authorities and reputable pollsters.",
    )
