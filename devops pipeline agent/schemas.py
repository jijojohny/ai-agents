from typing import List

from pydantic import BaseModel, Field


class PipelineSketchReply(BaseModel):
    stack_summary: str = Field(default="", description="Language, cloud, artifact registry")
    triggers: List[str] = Field(default_factory=list, description="on push, PR, tag, schedule")
    jobs: List[str] = Field(default_factory=list, description="Named steps: lint, test, build, deploy")
    secrets_handling: List[str] = Field(default_factory=list)
    caching_notes: List[str] = Field(default_factory=list)
    example_yaml_outline: str = Field(
        default="",
        description="Comment-rich skeleton — user must validate against vendor docs",
    )
    open_questions: List[str] = Field(default_factory=list)
