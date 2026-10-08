"""Error message UX structured reply."""
from typing import List, Optional

from pydantic import BaseModel, Field


class ErrorMessageUxReply(BaseModel):
    context: str = Field(description="Where the error appears")
    user_facing_title: str = Field(default="")
    user_facing_body: str = Field(default="")
    recovery_actions: List[str] = Field(default_factory=list)
    tone_notes: List[str] = Field(default_factory=list)
    what_not_to_expose: List[str] = Field(
        default_factory=list,
        description="Stack traces, secrets, internal IDs to hide",
    )
    log_or_support_hints: List[str] = Field(default_factory=list)
    alternatives: List[str] = Field(default_factory=list, description="Alternate copy options")
    severity: Optional[str] = Field(default=None, description="info | warning | error | critical")
