"""
Tools for fetching and parsing web pages (HTTP + HTML text extraction).
"""
from __future__ import annotations

from typing import List
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; WebScrapingAgent/1.0; educational/research; "
        "+https://github.com)"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
DEFAULT_TIMEOUT = 30


def _fetch_response(url: str) -> requests.Response:
    if not url.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=DEFAULT_TIMEOUT)
    resp.raise_for_status()
    return resp


def fetch_webpage_text_impl(url: str, max_characters: int = 15000) -> str:
    """Programmatic fetch + HTML-to-text (used by the tool and by quick_extract)."""
    try:
        resp = _fetch_response(url)
        ctype = resp.headers.get("Content-Type", "")
        if "text/html" not in ctype and "application/xhtml" not in ctype:
            # Still try to parse as HTML if server mislabels; otherwise return raw snippet
            text = resp.text[:max_characters]
            return f"URL: {url}\nContent-Type: {ctype}\nNote: non-HTML; raw snippet:\n{text}"

        soup = BeautifulSoup(resp.content, "lxml")
        for tag in soup(["script", "style", "noscript", "iframe"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        lines = [ln for ln in text.splitlines() if ln.strip()]
        text = "\n".join(lines)
        truncated = False
        if len(text) > max_characters:
            text = text[:max_characters]
            truncated = True
        suffix = "\n\n[... truncated ...]" if truncated else ""
        return f"URL: {url}\nHTTP {resp.status_code}\n\n{text}{suffix}"
    except requests.RequestException as e:
        return f"URL: {url}\nError fetching page: {e}"
    except Exception as e:
        return f"URL: {url}\nError parsing page: {e}"


@tool
def fetch_webpage_text(url: str, max_characters: int = 15000) -> str:
    """Fetch a web page URL and return extracted plain text (scripts/styles removed).

    Use for reading article body, docs, or listing pages. Respect the site's terms
    and robots.txt. Only use publicly accessible http(s) URLs.

    Args:
        url: Full http(s) URL to fetch.
        max_characters: Truncate extracted text to this length to fit context windows.
    """
    return fetch_webpage_text_impl(url, max_characters=max_characters)


@tool
def list_page_links(url: str, same_domain_only: bool = True, limit: int = 40) -> str:
    """List hyperlinks found on a page (useful before fetching related pages).

    Args:
        url: Page to parse for <a href> links.
        same_domain_only: If true, only return links on the same host as url.
        limit: Maximum number of links to return.
    """
    try:
        resp = _fetch_response(url)
        soup = BeautifulSoup(resp.content, "lxml")
        base = urlparse(url)
        seen: set[str] = set()
        out: List[str] = []
        for a in soup.find_all("a", href=True):
            href = urljoin(url, a["href"].strip())
            if not href.startswith(("http://", "https://")):
                continue
            if same_domain_only and urlparse(href).netloc.lower() != base.netloc.lower():
                continue
            if href in seen:
                continue
            seen.add(href)
            out.append(href)
            if len(out) >= limit:
                break
        if not out:
            return f"No links found (same_domain_only={same_domain_only}) for {url}"
        return "Links:\n" + "\n".join(out)
    except Exception as e:
        return f"Error listing links for {url}: {e}"


def get_scraping_tools():
    """Tools passed to the LangChain agent."""
    return [fetch_webpage_text, list_page_links]
