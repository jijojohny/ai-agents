"""Onboarding guide structured reply."""
from typing import List, Optional

from pydantic import BaseModel, Field


class OnboardingGuideReply(BaseModel):
    audience: str = Field(description="Who is being onboarded")
    goals: List[str] = Field(default_factory=list)
    day_one: List[str] = Field(default_factory=list)
    first_week: List[str] = Field(default_factory=list)
    first_month: List[str] = Field(default_factory=list)
    checklist: List[str] = Field(default_factory=list)
    owner_roles: List[str] = Field(
        default_factory=list,
        description="Who owns each onboarding track (manager, buddy, IT)",
    )
    risks: List[str] = Field(default_factory=list)
    markdown_guide: Optional[str] = Field(default=None, description="Full markdown outline")
