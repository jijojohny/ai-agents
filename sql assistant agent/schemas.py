"""SQL assistant structured reply."""
from typing import List

from pydantic import BaseModel, Field


class SQLAssistantReply(BaseModel):
    dialect: str = Field(default="ansi", description="postgres, mysql, sqlite, bigquery, snowflake, etc.")
    intent_summary: str = Field(description="What the query does in plain language")
    sql: str = Field(description="Suggested SQL (read-only by policy)")
    assumptions: List[str] = Field(default_factory=list, description="Schema guesses or missing info")
    safety_notes: List[str] = Field(
        default_factory=list,
        description="Injection, LIMIT, permissions, PII",
    )
