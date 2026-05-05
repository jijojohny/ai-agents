from typing import List

from pydantic import BaseModel, Field


class ComposeSketchReply(BaseModel):
    summary: str = Field(default="")
    services: List[str] = Field(
        default_factory=list,
        description="yaml-ish lines or pseudo-blocks per service",
    )
    networks: List[str] = Field(default_factory=list)
    volumes: List[str] = Field(default_factory=list)
    env_and_secrets_notes: List[str] = Field(default_factory=list)
    caveats: List[str] = Field(
        default_factory=list,
        description="Version pins, host paths, prod vs dev",
    )
