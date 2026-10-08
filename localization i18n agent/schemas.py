"""Localization / i18n structured reply."""
from typing import List, Optional

from pydantic import BaseModel, Field


class LocalizationI18nReply(BaseModel):
    locales: List[str] = Field(default_factory=list, description="Target locales (BCP-47)")
    copy_inventory: List[str] = Field(
        default_factory=list,
        description="UI strings / keys to extract or translate",
    )
    message_key_suggestions: List[str] = Field(default_factory=list)
    pluralization_notes: List[str] = Field(default_factory=list)
    formatting_notes: List[str] = Field(
        default_factory=list,
        description="Dates, numbers, currency, RTL, etc.",
    )
    glossary: List[str] = Field(default_factory=list, description="term = preferred translation notes")
    risks: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)
    sample_json_catalog: Optional[str] = Field(
        default=None,
        description="Optional JSON message catalog sketch",
    )
