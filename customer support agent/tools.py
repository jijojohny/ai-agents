"""
Tools for customer support workflows.
"""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def categorize_issue(message: str) -> str:
    """Classify a support message into a simple issue category for routing."""
    text = (message or "").lower()
    if any(k in text for k in ("refund", "charged", "billing", "invoice", "payment")):
        return "billing"
    if any(k in text for k in ("broken", "damaged", "defect", "not working", "faulty")):
        return "product_quality"
    if any(k in text for k in ("late", "delivery", "shipping", "tracking", "package")):
        return "shipping"
    if any(k in text for k in ("login", "password", "account", "sign in", "locked")):
        return "account_access"
    return "general_support"


@tool
def generate_refund_checklist(order_id: str, reason: str) -> str:
    """Return a concise checklist for a standard refund intake flow."""
    oid = (order_id or "").strip() or "<missing_order_id>"
    why = (reason or "").strip() or "<missing_reason>"
    return (
        "Refund intake checklist:\n"
        f"1) Confirm order id: {oid}\n"
        f"2) Capture reason: {why}\n"
        "3) Verify purchase date and payment method\n"
        "4) Request photo evidence if item is damaged/incorrect\n"
        "5) Confirm refund destination and expected timeline\n"
        "6) Escalate to billing team if duplicate charge is suspected"
    )


def get_customer_support_tools():
    return [categorize_issue, generate_refund_checklist]
