"""i18n planning reference tools."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def i18n_checklist() -> str:
    """Checklist for shipping a localized product surface."""
    return (
        "i18n checklist:\n"
        "- Externalize user-facing strings (no concatenation of sentences)\n"
        "- Message keys with context comments for translators\n"
        "- Plural rules (CLDR) and gender/select where needed\n"
        "- Locale-aware dates, numbers, currency, units\n"
        "- RTL layout (mirroring, icons, punctuation)\n"
        "- Pseudo-localization for UI overflow testing\n"
        "- Avoid hardcoded locale in URLs/emails unless intentional"
    )


@tool
def localization_anti_patterns() -> str:
    """Common localization mistakes."""
    return (
        "Avoid:\n"
        "- Splitting sentences across keys\n"
        "- Machine-translating legal/medical without review\n"
        "- Inventing official translations for brand terms\n"
        "- Assuming one language = one country\n"
        "- Hardcoding en-US formats for all users"
    )


def get_localization_i18n_tools():
    return [i18n_checklist, localization_anti_patterns]
