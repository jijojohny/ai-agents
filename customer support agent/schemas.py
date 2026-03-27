"""Optional structured schema for support responses."""
from typing import List

from pydantic import BaseModel, Field


class SupportReply(BaseModel):
    issue_category: str = Field(description="Detected category: billing, shipping, etc.")
    customer_message: str = Field(description="Human-friendly response to the customer")
    next_actions: List[str] = Field(default_factory=list, description="Actionable next steps")
    escalation_needed: bool = Field(
        default=False,
        description="Whether this issue should be escalated to another team",
    )
