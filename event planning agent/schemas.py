from typing import List

from pydantic import BaseModel, Field


class EventPlanReply(BaseModel):
    event_summary: str = Field(default="")
    audience_and_goals: str = Field(default="")
    timeline_phases: List[str] = Field(
        default_factory=list,
        description="Pre-event / day-of / post-event chunks",
    )
    run_of_show: List[str] = Field(
        default_factory=list,
        description="Time-ordered items with duration hints when possible",
    )
    logistics_checklist: List[str] = Field(default_factory=list)
    risks_contingencies: List[str] = Field(default_factory=list)
