"""Database schema design structured reply."""
from typing import List, Optional

from pydantic import BaseModel, Field


class TableSketch(BaseModel):
    name: str
    purpose: str = ""
    columns: List[str] = Field(default_factory=list, description="name type notes")
    indexes: List[str] = Field(default_factory=list)
    relationships: List[str] = Field(default_factory=list)


class DatabaseSchemaDesignReply(BaseModel):
    dialect: str = Field(default="postgres", description="Target SQL dialect / store")
    overview: str = Field(description="High-level data model summary")
    tables: List[TableSketch] = Field(default_factory=list)
    constraints_notes: List[str] = Field(default_factory=list)
    migration_notes: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)
    ddl_sketch: Optional[str] = Field(
        default=None,
        description="Optional CREATE TABLE sketch (non-destructive suggestion)",
    )
