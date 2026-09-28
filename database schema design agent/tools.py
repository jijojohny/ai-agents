"""Schema design reference tools."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def schema_design_checklist() -> str:
    """Checklist for relational schema sketches."""
    return (
        "Schema design checklist:\n"
        "- Entities, primary keys, foreign keys\n"
        "- Nullability and uniqueness constraints\n"
        "- Indexes for common filters/joins (justify)\n"
        "- Soft deletes vs hard deletes\n"
        "- Timestamps (created_at/updated_at) and timezone policy\n"
        "- Multi-tenancy strategy if needed\n"
        "- Naming consistency (snake_case tables/columns)"
    )


@tool
def normalization_tradeoffs() -> str:
    """When to normalize vs denormalize."""
    return (
        "Normalize to reduce update anomalies; denormalize for read-heavy hot paths "
        "with clear consistency ownership. Document write amplification and cache invalidation. "
        "Prefer explicit join tables for many-to-many. Avoid premature sharding in sketches."
    )


def get_database_schema_design_tools():
    return [schema_design_checklist, normalization_tradeoffs]
