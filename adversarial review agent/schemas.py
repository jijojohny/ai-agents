"""Structured final output from the chair (synthesis) phase."""
from typing import List

from pydantic import BaseModel, Field


class AdversarialReviewReport(BaseModel):
    analyst_summary: str = Field(description="Neutral decomposition of the proposal")
    red_team_risks: List[str] = Field(
        default_factory=list,
        description="Failure modes, abuse cases, second-order effects",
    )
    blue_team_mitigations: List[str] = Field(
        default_factory=list,
        description="Controls, monitoring, guardrails, rollout strategy",
    )
    chair_verdict: str = Field(description="Balanced recommendation in plain language")
    confidence: str = Field(
        default="medium",
        description="low | medium | high (model may use variants)",
    )
    next_steps: List[str] = Field(default_factory=list, description="Concrete next actions")
    open_questions: List[str] = Field(
        default_factory=list,
        description="What must be validated before committing",
    )
