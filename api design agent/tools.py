"""API design reference tools."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def rest_status_cheatsheet() -> str:
    """Common HTTP status usage for REST-ish APIs."""
    return (
        "Status hints:\n"
        "- 200 OK: success with body\n"
        "- 201 Created: resource created (Location header optional)\n"
        "- 204 No Content: success, no body\n"
        "- 400 Bad Request: validation / malformed\n"
        "- 401 Unauthorized: not authenticated\n"
        "- 403 Forbidden: authenticated but not allowed\n"
        "- 404 Not Found: missing resource\n"
        "- 409 Conflict: state conflict (dup, concurrency)\n"
        "- 422 Unprocessable: semantic validation (if you use it)\n"
        "- 429 Too Many Requests: rate limit\n"
        "- 500/503: server errors — avoid leaking internals"
    )


@tool
def api_idempotency_reminder() -> str:
    """Safe retries for writes."""
    return (
        "Idempotency:\n"
        "- Use Idempotency-Key for POST that creates billing/state\n"
        "- PUT/PATCH to same URL should be safe to retry when documented\n"
        "- GET/HEAD/OPTIONS/PUT/DELETE are often idempotent by design\n"
        "Document which operations are not safe to retry."
    )


def get_api_design_tools():
    return [rest_status_cheatsheet, api_idempotency_reminder]
