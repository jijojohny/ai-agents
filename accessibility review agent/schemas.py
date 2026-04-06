"""Accessibility review structured output."""
from typing import List

from pydantic import BaseModel, Field


class A11yIssue(BaseModel):
    area: str = Field(description="Screen, component, or flow")
    issue: str = Field(description="Barrier or failure mode")
    severity: str = Field(default="medium", description="critical|serious|moderate|low")
    recommendation: str = Field(default="", description="Fix or test step")


class A11yReviewReply(BaseModel):
    summary: str = Field(description="Executive summary")
    issues: List[A11yIssue] = Field(default_factory=list)
    quick_wins: List[str] = Field(default_factory=list)
    testing_suggestions: List[str] = Field(
        default_factory=list,
        description="Keyboard, screen reader, contrast tools",
    )
    disclaimer: str = Field(
        default="Not a formal WCAG audit; validate with experts and automated tools.",
    )
