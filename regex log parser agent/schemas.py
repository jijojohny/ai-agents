from typing import List

from pydantic import BaseModel, Field


class LogParseReply(BaseModel):
    intent_summary: str = Field(default="", description="What fields or lines to capture")
    suggested_pattern: str = Field(default="", description="Regex or grep-style pattern")
    pattern_explanation: str = Field(default="", description="Step through groups/literals")
    test_strings: List[str] = Field(default_factory=list, description="Lines to try against")
    pitfalls: List[str] = Field(default_factory=list, description="ReDoS, greedy vs lazy, multiline")
