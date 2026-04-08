"""Structured API design sketch."""
from typing import List

from pydantic import BaseModel, Field


class ApiDesignReply(BaseModel):
    overview: str = Field(description="Problem, consumers, non-goals")
    resources: List[str] = Field(default_factory=list, description="Core nouns / collections")
    endpoints: List[str] = Field(
        default_factory=list,
        description="METHOD path — purpose (one line each)",
    )
    auth_security: List[str] = Field(default_factory=list, description="AuthN/Z, scopes, rate limits")
    errors_and_pagination: List[str] = Field(
        default_factory=list,
        description="Error envelope, idempotency, cursor vs offset",
    )
    versioning: str = Field(default="", description="URL vs header versioning recommendation")
    open_questions: List[str] = Field(default_factory=list)
