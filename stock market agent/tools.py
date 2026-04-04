"""
Stock data tools via yfinance (Yahoo Finance public endpoints — may be delayed; not real-time for all venues).
"""
from __future__ import annotations

from typing import List

from langchain_core.tools import tool

_VALID_PERIODS = frozenset({"1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"})


def _ticker(symbol: str):
    try:
        import yfinance as yf
    except ImportError as e:
        raise ImportError(
            "yfinance is required. pip install yfinance pandas"
        ) from e
    sym = (symbol or "").strip().upper()
    if not sym:
        raise ValueError("symbol is empty")
    return yf.Ticker(sym), sym


@tool
def get_stock_quote(symbol: str) -> str:
    """Latest quote-style snapshot: last price, previous close, day range, volume (best effort via yfinance).

    Args:
        symbol: Equity ticker, e.g. AAPL, MSFT, ^GSPC for S&P 500 index.
    """
    try:
        t, sym = _ticker(symbol)
        lines: List[str] = [f"Symbol: {sym}"]

        try:
            fi = t.fast_info
            for attr in ("last_price", "previous_close", "open", "day_high", "day_low", "last_volume"):
                v = getattr(fi, attr, None)
                if v is not None:
                    lines.append(f"{attr}: {v}")
        except Exception:
            pass

        hist = t.history(period="5d")
        if hist is not None and not hist.empty:
            last = hist.iloc[-1]
            lines.append(
                f"history_last_close: {float(last['Close']):.4f} on {hist.index[-1].strftime('%Y-%m-%d')}"
            )
            if len(hist) >= 2:
                prev = hist.iloc[-2]["Close"]
                chg = (float(last["Close"]) - float(prev)) / float(prev) * 100.0
                lines.append(f"approx_5d_change_pct: {chg:.2f}%")
        else:
            lines.append("history: (empty — verify ticker or market hours)")

        return "\n".join(lines)
    except Exception as e:
        return f"Error get_stock_quote({symbol}): {e}"


@tool
def get_stock_history(symbol: str, period: str = "3mo", interval: str = "1d") -> str:
    """OHLCV history summary: date range, row count, last rows, and simple return vs start of period.

    Args:
        symbol: Ticker symbol.
        period: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        interval: 1d,1wk,1mo (intraday intervals may fail for long periods)
    """
    try:
        per = (period or "3mo").strip().lower()
        if per not in _VALID_PERIODS:
            per = "3mo"
        iv = (interval or "1d").strip().lower()
        t, sym = _ticker(symbol)
        hist = t.history(period=per, interval=iv, auto_adjust=True)
        if hist is None or hist.empty:
            return f"{sym}: no history returned for period={per} interval={iv}"

        first = hist.iloc[0]
        last = hist.iloc[-1]
        start = float(first["Close"])
        end = float(last["Close"])
        ret = (end - start) / start * 100.0 if start else 0.0
        hi = float(hist["High"].max())
        lo = float(hist["Low"].min())

        tail = hist.tail(5).to_string()
        return (
            f"Symbol: {sym} period={per} interval={iv} rows={len(hist)}\n"
            f"range: {hist.index[0]} .. {hist.index[-1]}\n"
            f"period_return_pct: {ret:.2f}%  period_high: {hi:.4f}  period_low: {lo:.4f}\n"
            f"last_5_rows:\n{tail}"
        )
    except Exception as e:
        return f"Error get_stock_history({symbol}): {e}"


@tool
def get_stock_profile(symbol: str) -> str:
    """Company/fund profile fields from yfinance .info (when available): sector, industry, marketCap, trailing PE, etc."""
    try:
        t, sym = _ticker(symbol)
        info = t.info or {}
        if not info:
            return f"{sym}: empty .info (API may be rate-limited or symbol invalid)"

        keys = [
            "longName",
            "shortName",
            "quoteType",
            "exchange",
            "currency",
            "sector",
            "industry",
            "marketCap",
            "trailingPE",
            "forwardPE",
            "dividendYield",
            "fiftyTwoWeekHigh",
            "fiftyTwoWeekLow",
            "averageVolume",
            "website",
        ]
        lines = [f"Symbol: {sym}"]
        for k in keys:
            if k in info and info[k] is not None:
                lines.append(f"{k}: {info[k]}")
        return "\n".join(lines) if len(lines) > 1 else f"{sym}: no profile keys found"
    except Exception as e:
        return f"Error get_stock_profile({symbol}): {e}"


@tool
def get_stock_news(symbol: str, max_items: int = 5) -> str:
    """Recent headlines/snippets linked to the ticker (provider-dependent; may be sparse)."""
    try:
        t, sym = _ticker(symbol)
        n = max(1, min(int(max_items), 15))
        items = t.news or []
        if not items:
            return f"{sym}: no news items returned"
        lines = [f"Symbol: {sym} (up to {n} items)"]
        for i, it in enumerate(items[:n]):
            title = it.get("title") or ""
            pub = it.get("publisher") or ""
            link = it.get("link") or ""
            lines.append(f"{i + 1}. {title} — {pub}\n   {link}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error get_stock_news({symbol}): {e}"


def get_stock_market_tools():
    return [get_stock_quote, get_stock_history, get_stock_profile, get_stock_news]
