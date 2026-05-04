"""Multi-provider chat model factory."""
from __future__ import annotations

import os
from typing import Any, Optional

_D = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-sonnet-20241022",
    "google": "gemini-2.0-flash",
    "gemini": "gemini-2.0-flash",
    "vertex": "gemini-2.0-flash",
}


def _m(provider: str, model_name: Optional[str]) -> str:
    if model_name and str(model_name).strip():
        return str(model_name).strip()
    e = os.getenv("GRANT_PROPOSAL_AGENT_MODEL")
    return e.strip() if e else _D.get(provider, _D["openai"])


def build_chat_model(provider: str, model_name: Optional[str] = None, temperature: float = 0.3) -> Any:
    p = (provider or "openai").strip().lower()
    if p == "gemini":
        p = "google"
    m = _m(p, model_name)
    if p == "openai":
        from langchain_openai import ChatOpenAI
        k = os.getenv("OPENAI_API_KEY")
        if not k:
            raise ValueError("OPENAI_API_KEY is not set.")
        return ChatOpenAI(model=m, temperature=temperature, api_key=k)
    if p == "anthropic":
        from langchain_anthropic import ChatAnthropic
        k = os.getenv("ANTHROPIC_API_KEY")
        if not k:
            raise ValueError("ANTHROPIC_API_KEY is not set.")
        return ChatAnthropic(model=m, temperature=temperature, api_key=k)
    if p == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        k = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not k:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY is not set.")
        return ChatGoogleGenerativeAI(model=m, temperature=temperature, google_api_key=k)
    if p == "vertex":
        from langchain_google_vertexai import ChatVertexAI
        pr = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT") or os.getenv("VERTEX_PROJECT")
        lo = os.getenv("GOOGLE_CLOUD_LOCATION") or os.getenv("VERTEX_LOCATION") or "us-central1"
        if not pr:
            raise ValueError("Vertex project not set.")
        return ChatVertexAI(model=m, temperature=temperature, project=pr, location=lo)
    raise ValueError(f"Unknown provider: {provider}")
