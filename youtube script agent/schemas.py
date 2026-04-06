"""Structured YouTube content package."""
from typing import List

from pydantic import BaseModel, Field


class YouTubeScriptReply(BaseModel):
    title_options: List[str] = Field(default_factory=list, description="3 title ideas")
    hook: str = Field(description="First 15–30s hook script")
    outline: List[str] = Field(default_factory=list, description="Chapter / beat list")
    script_beats: List[str] = Field(
        default_factory=list,
        description="Talking points or paragraph beats",
    )
    cta: str = Field(default="", description="Subscribe, link, next video")
    description_snippet: str = Field(default="", description="Short description + keywords hint")
    retention_tips: List[str] = Field(default_factory=list)
