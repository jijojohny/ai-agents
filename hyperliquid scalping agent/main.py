"""
Hyperliquid BTC Scalping Agent — AI-powered multi-strategy scalping bot.

Strategies:
  1. Momentum Scalp          – EMA crossover + MACD + RSI alignment
  2. Mean Reversion           – Bollinger Band extremes + RSI divergence
  3. Volatility Squeeze       – BB/KC squeeze breakout
  4. Order Flow Imbalance     – CVD delta + order book walls
  5. Multi-TF Confluence      – HTF trend + LTF entry trigger
  6. Funding Rate Fade        – Overcrowded-position fade
  7. Liquidity Sweep / BOS    – Sweep of swing high/low + structure break
"""
import os
import json
import time
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.agents import create_agent

from tools import (
    HyperliquidClient,
    HyperliquidConfig,
    create_scalping_tools,
    TechnicalAnalyzer,
    MultiTimeframeEngine,
    SessionFilter,
    TrailingStopManager,
    EquityCurveProtector,
)
from schemas import AgentState, TradeRecord

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


# ---------------------------------------------------------------------------
# System prompt with full 7 strategies
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an elite BTC scalping agent on Hyperliquid with 7 advanced strategies at your disposal.
You analyse the market using every available tool and pick the highest-probability setup.

═══════════════════════════════════════════════════════════════
FEE AWARENESS — CRITICAL FOR PROFITABILITY
═══════════════════════════════════════════════════════════════
Hyperliquid fees:
  Taker (market orders): 0.035% per side → 0.07% round-trip (entry + exit)
  Maker (limit orders) : 0.01%  per side → 0.02% round-trip (entry + exit)

EVERY trade must clear the round-trip fee to be profitable:
  - Market order trade: TP must be > 0.07% to break even. Target TP ≥ 0.15% minimum.
  - Limit order trade : TP must be > 0.02% to break even. Target TP ≥ 0.10% minimum.
  - ALWAYS prefer limit orders when spread and conditions allow — they cost 3.5× less in fees.
  - When the execute_order result returns fee details, verify net profit > 0.
  - For small accounts, fees consume a larger % of equity. Be extra selective with entries.
  - Factor fees into EVERY risk/reward calculation: actual R:R = (TP - fees) / (SL + fees).

═══════════════════════════════════════════════════════════════
STRATEGY 1 — MOMENTUM SCALP
═══════════════════════════════════════════════════════════════
WHEN: ADX > 25, EMA 9/21 aligned, MACD histogram same direction, Supertrend agrees.
LONG : EMA 9 > EMA 21, MACD histogram positive & rising, RSI 40-65, Supertrend bullish.
SHORT: EMA 9 < EMA 21, MACD histogram negative & falling, RSI 35-60, Supertrend bearish.
TP: 0.4-0.6% (1.5× ATR).  SL: 0.2-0.3% (1× ATR).  Hold: 2-10 min.

═══════════════════════════════════════════════════════════════
STRATEGY 2 — MEAN REVERSION
═══════════════════════════════════════════════════════════════
WHEN: ADX < 20 (ranging), price at Bollinger Band extreme, RSI divergence present.
LONG : Price touches/breaks lower BB, RSI < 30 or bullish RSI divergence, CMF turning positive.
SHORT: Price touches/breaks upper BB, RSI > 70 or bearish RSI divergence, CMF turning negative.
TP: Return to BB middle (SMA 20).  SL: 0.3% beyond the touched band.  Hold: 3-15 min.
Confirm with Stochastic RSI reversal signal and Heikin Ashi colour flip.

═══════════════════════════════════════════════════════════════
STRATEGY 3 — VOLATILITY SQUEEZE BREAKOUT
═══════════════════════════════════════════════════════════════
WHEN: Bollinger Bands inside Keltner Channel (squeeze_on = True), then squeeze releases.
LONG : squeeze_fire_long — momentum positive and rising after squeeze.
SHORT: squeeze_fire_short — momentum negative and falling after squeeze.
TP: 0.5-0.8% (2× ATR) — breakout moves are larger.  SL: 0.3% (back inside squeeze zone).
Confirm with OBV trend and order flow delta agreement.

═══════════════════════════════════════════════════════════════
STRATEGY 4 — ORDER FLOW IMBALANCE
═══════════════════════════════════════════════════════════════
WHEN: Order book imbalance > 2.0 or < 0.5, CVD trend strong, large trades detected.
LONG : Strong buying CVD, bid depth >> ask depth, large buy trades, price near bid wall support.
SHORT: Strong selling CVD, ask depth >> bid depth, large sell trades, price near ask wall resistance.
TP: 0.3-0.5%.  SL: 0.2%.  Hold: 1-5 min — these are fast momentum plays.
Confirm with spread tightness (< 3 bps).

═══════════════════════════════════════════════════════════════
STRATEGY 5 — MULTI-TIMEFRAME CONFLUENCE
═══════════════════════════════════════════════════════════════
WHEN: 1h + 15m trends aligned, 5m gives entry signal, confluence ≥ strong_bullish/strong_bearish.
LONG : HTF bias bullish, 5m EMA crossover up, 1m RSI pulling back to 40-50 zone.
SHORT: HTF bias bearish, 5m EMA crossover down, 1m RSI pulling back to 50-60 zone.
TP: 0.5-0.7%.  SL: 0.3%.  Hold: 5-15 min.
Confirm with Ichimoku cloud signal on 15m.

═══════════════════════════════════════════════════════════════
STRATEGY 6 — FUNDING RATE FADE
═══════════════════════════════════════════════════════════════
WHEN: Extreme funding rate (> 0.05% or < -0.05% hourly), price at resistance/support.
LONG : Extreme negative funding (shorts paying), price at support, bearish sentiment = fade it.
SHORT: Extreme positive funding (longs paying), price at resistance, bullish sentiment = fade it.
TP: 0.4-0.6%.  SL: 0.3%.  Hold: 5-20 min — timing around funding interval.
Confirm with Pivot Point proximity and order flow agreement.

═══════════════════════════════════════════════════════════════
STRATEGY 7 — LIQUIDITY SWEEP / MARKET STRUCTURE BREAK
═══════════════════════════════════════════════════════════════
WHEN: Price sweeps a swing high/low then reverses, confirmed by Break of Structure (BOS).
LONG : Price sweeps below a swing low (liquidity grab), immediately reclaims, bullish BOS detected.
         Fibonacci 61.8-78.6% retracement zone as entry.
SHORT: Price sweeps above a swing high, immediately rejects, bearish BOS detected.
         Fibonacci 61.8-78.6% retracement zone as entry.
TP: Previous swing high/low.  SL: Beyond the swept level.  Hold: 5-15 min.
Confirm with Heikin Ashi reversal candle and OBV divergence.

═══════════════════════════════════════════════════════════════
CRITICAL RULES
═══════════════════════════════════════════════════════════════
1. ALWAYS call get_market_data first. NEVER trade without fresh data.
2. ALWAYS call multi_timeframe_analysis to check HTF alignment before entry.
3. Call get_funding_rate when considering strategy 6, or to sanity-check any trade.
4. ALWAYS call get_position before opening or closing. NEVER stack positions.
5. ALWAYS call risk_check before calling execute_order. If it fails, do NOT trade.
6. Maximum 1 open position at a time.
7. Never fight the higher-timeframe trend unless running strategy 2 or 6 in a range.
8. Skip trading outside kill zones unless signal is very_high confidence.
9. Prefer strategies where multiple signals agree (≥ 3 supporting indicators).
10. If trailing stop says should_close=True, close immediately.
11. Use partial_close (50-70%) at first TP, let remainder run with trailing stop.
12. FEES: Every TP target MUST clear the round-trip fee (0.07% for market, 0.02% for limit).
    Actual R:R = (TP% - round_trip_fee%) / (SL% + round_trip_fee%). If R:R < 1.5, skip the trade.
13. PREFER limit orders over market orders when spread is tight — saves 3.5× in fees.
14. After execute_order, check the "fees" field in the response. If net profit after fees is
    negative or marginal, tighten your entry criteria.

═══════════════════════════════════════════════════════════════
7-STEP REASONING PROCESS
═══════════════════════════════════════════════════════════════
STEP 1 — MARKET ANALYSIS: Call get_market_data. Digest ALL indicators. Determine regime.
STEP 2 — MULTI-TIMEFRAME: Call multi_timeframe_analysis + get_funding_rate. Note HTF bias.
STEP 3 — SIGNAL DETECTION: Score each signal type. Calculate combined signal score (-100 to +100).
STEP 4 — STRATEGY SELECTION: Pick the best strategy. Explain why, list supporting & conflicting signals.
STEP 5 — RISK SIZING: Calculate position size from ATR. Dynamic SL = 1-1.5× ATR, TP = 1.5-2.5× ATR.
           Adjust leverage inversely to volatility.  Plan partial TP levels.
           Calculate fee-adjusted R:R: (TP - 0.07%) / (SL + 0.07%) for market orders.
           If fee-adjusted R:R < 1.5, DO NOT take the trade.
STEP 6 — EXECUTION: Call risk_check, then execute_order if passed.  Use limit order if spread allows.
           After execution, verify the fee summary shows net profit > 0.
STEP 7 — POST-TRADE REVIEW: Summarize what was done and why.  Include fee impact on P&L.

Return structured reasoning for every step.  Never skip a step.
"""


class BTCScalpingAgent:
    """AI-powered multi-strategy BTC scalping agent."""

    def __init__(
        self,
        model_name: str = "gpt-5.2",
        temperature: float = 0.1,
        verbose: bool = True,
    ):
        self.verbose = verbose
        self.config = HyperliquidConfig()
        self.client = HyperliquidClient(self.config)
        self.tools = create_scalping_tools(self.client)
        self.analyzer = TechnicalAnalyzer()
        self.mtf_engine = MultiTimeframeEngine(self.client)

        self.llm = ChatOpenAI(model=model_name, temperature=temperature)

        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
        )

        self.state = AgentState(session_start=datetime.now())
        self.chat_history: List = []

    # -- Logging --

    def log(self, message: str, level: str = "INFO"):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        icons = {"INFO": "ℹ️ ", "SUCCESS": "✅", "WARNING": "⚠️ ", "ERROR": "❌", "TRADE": "💰", "STRATEGY": "🎯"}
        if self.verbose:
            print(f"[{ts}] {icons.get(level, '')} {message}")

    # -- Core cycle methods --

    def analyze_market(self) -> Dict:
        self.log("Starting full market analysis", "INFO")

        session = SessionFilter.current_session()
        session_str = (
            f"UTC hour: {session['utc_hour']}, "
            f"Sessions: {', '.join(session['active_sessions']) or 'none'}, "
            f"Kill zones: {', '.join(session['in_kill_zone']) or 'none'}, "
            f"Vol factor: {session['volatility_factor']}"
        )

        prompt = f"""Perform a complete 7-step analysis for BTC scalping.

Current session context: {session_str}

Follow ALL 7 steps:
1. Call get_market_data to get all indicators, orderbook, order flow, and session data.
2. Call multi_timeframe_analysis for HTF confluence. Also call get_funding_rate.
3. Evaluate every signal category from step 1 and 2. Assign a combined signal score.
4. Select the BEST strategy (1-7) for current conditions. Explain supporting/conflicting signals.
5. Calculate dynamic position size, SL (ATR-based), TP (ATR-based), and partial TP levels.
6. Call get_position to check state, then risk_check. If passed, call execute_order.
7. Summarize what you did and why. Mention trailing stop and equity protection status.

If no clear setup exists (signal score between -30 and +30), say "NO TRADE" and explain why.
If you call execute_order, ALWAYS report the exact exchange response including any errors.
If the order fails (e.g. insufficient margin), say "ORDER FAILED" and include the error.

Timestamp: {datetime.now().isoformat()}
"""
        try:
            messages = self.chat_history[-10:] + [HumanMessage(content=prompt)]
            result = self.agent.invoke({"messages": messages})
            output_messages = result.get("messages", [])
            output = output_messages[-1].content if output_messages else ""

            self.chat_history.append(HumanMessage(content=prompt))
            self.chat_history.append(AIMessage(content=output))
            if len(self.chat_history) > 30:
                self.chat_history = self.chat_history[-30:]

            return {"success": True, "output": output, "timestamp": datetime.now().isoformat()}
        except Exception as e:
            self.log(f"Analysis error: {e}", "ERROR")
            return {"success": False, "error": str(e), "timestamp": datetime.now().isoformat()}

    def check_position_management(self) -> Dict:
        position = self.client.get_position("BTC")
        if not position:
            return {"has_position": False, "action": "none"}

        prompt = """We have an open BTC position that needs active management.

Follow these steps:
1. Call get_position to get full position state, trailing stop info, and equity protection.
2. Call get_market_data to get fresh indicators and order flow.
3. Evaluate:
   a) Has the trailing stop activated? If should_close=True, IMMEDIATELY call execute_order action='close'.
   b) Has the take-profit zone been reached? Consider partial_close (close_pct=0.5).
   c) Has the signal reversed? (e.g. EMA crossover flipped, MACD histogram changed sign).
   d) Has the stop loss been breached?
   e) Is the position stale? (held > 10 min without meaningful profit).
4. If closing or partial-closing, call execute_order.
5. If holding, explain why signals still support the position.

Be decisive. Cut losses fast. Let winners run with trailing stop."""

        try:
            messages = self.chat_history[-5:] + [HumanMessage(content=prompt)]
            result = self.agent.invoke({"messages": messages})
            output_messages = result.get("messages", [])
            output = output_messages[-1].content if output_messages else ""

            if any(kw in output.lower() for kw in ['"filled"', '"totalsz"', "order #"]):
                self.state.total_trades += 1
                self.log("Position closed/adjusted — FILLED on exchange", "TRADE")
            elif any(kw in output.lower() for kw in ["close", "stopped", "partial_close"]):
                self.log("Close signal detected (check exchange for fill confirmation)", "INFO")

            return {"has_position": True, "output": output, "timestamp": datetime.now().isoformat()}
        except Exception as e:
            self.log(f"Position management error: {e}", "ERROR")
            return {"has_position": True, "error": str(e)}

    def run_single_cycle(self) -> Dict:
        self.log("=" * 60, "INFO")
        self.log("Starting trading cycle", "INFO")

        pos_check = self.check_position_management()
        if pos_check.get("has_position"):
            self.log("Managed existing position", "INFO")
            return pos_check

        user_state = self.client.get_user_state()
        equity = 0
        if user_state and "marginSummary" in user_state:
            equity = float(user_state["marginSummary"].get("accountValue", 0))
        if equity <= 0:
            self.log("Account equity is $0 — cannot trade. Deposit USDC to your Hyperliquid account.", "WARNING")
            self.log("Running analysis in read-only mode (no orders will be placed).", "INFO")

        analysis = self.analyze_market()
        if analysis.get("success"):
            output = analysis.get("output", "").lower()

            for strat in ["momentum_scalp", "mean_reversion", "volatility_squeeze",
                          "order_flow", "multi_timeframe", "funding_rate", "liquidity_sweep"]:
                if strat.replace("_", " ") in output or strat in output:
                    self.state.active_strategy = strat
                    self.log(f"Strategy: {strat}", "STRATEGY")
                    break

            actually_filled = any(kw in output for kw in ['"filled"', '"totalSz"', '"avgPx"', "order #"])
            if actually_filled:
                self.state.total_trades += 1
                self.log(f"Trade #{self.state.total_trades} FILLED on exchange", "TRADE")
            elif any(kw in output for kw in ["execute_order", "order placed"]):
                if equity > 0:
                    self.log("Order sent (check position for fill status)", "INFO")
                else:
                    self.log("Order attempted but account has no equity — order will fail", "WARNING")
            elif "no trade" in output or "no_action" in output:
                self.log("No trade signal — waiting", "INFO")
        else:
            self.log(f"Analysis failed: {analysis.get('error')}", "ERROR")

        return analysis

    # -- Continuous loop --

    def run_continuous(self, interval_seconds: int = 30, max_cycles: Optional[int] = None):
        self.log("Starting multi-strategy scalping agent", "INFO")
        self.log(f"Network: {self.config.network}", "INFO")
        self.log(f"Interval: {interval_seconds}s", "INFO")
        self.log(f"Max position: ${self.config.max_position_size_usd}", "INFO")
        self.log(f"Leverage: {self.config.default_leverage}x", "INFO")
        self.log(f"TP: {self.config.take_profit_pct*100}%  SL: {self.config.stop_loss_pct*100}%", "INFO")
        self.log(f"Fees: taker {self.config.taker_fee_rate*100:.3f}%/side, "
                 f"maker {self.config.maker_fee_rate*100:.3f}%/side, "
                 f"RT taker {self.config.round_trip_taker_fee*100:.3f}%", "INFO")
        self.log(f"Trailing: activate {self.config.trailing_stop_activation_pct*100}%, "
                 f"distance {self.config.trailing_stop_distance_pct*100}%", "INFO")
        self.log(f"Max daily drawdown: {self.config.max_daily_drawdown_pct*100}%", "INFO")
        self.log(f"Strategies: Momentum | MeanRev | Squeeze | OrderFlow | MTF | FundingFade | LiqSweep", "INFO")

        status = self.get_status()
        equity = status.get("account_equity", 0)
        if equity > 0:
            import math
            mid = self.client.get_mid_price("BTC") or 80000
            min_notional = 0.001 * mid
            needed_lev = max(self.config.default_leverage, math.ceil(min_notional / equity))
            needed_lev = min(needed_lev, 50)
            if needed_lev > self.config.default_leverage:
                self.log(f"Small account: auto-adjusting leverage to {needed_lev}x for min order size", "WARN")
            lev_result = self.client.set_leverage("BTC", needed_lev, True)
            self.log(f"Leverage set to {needed_lev}x (cross): {lev_result.get('status', 'unknown')}", "INFO")

        self.client.subscribe_to_market_data("BTC")

        cycle = 0
        self.state.is_running = True

        try:
            while self.state.is_running:
                cycle += 1
                if max_cycles and cycle > max_cycles:
                    self.log(f"Max cycles ({max_cycles}) reached", "INFO")
                    break

                self.log(f"── Cycle {cycle} ──", "INFO")
                self.run_single_cycle()

                self.log(f"Sleeping {interval_seconds}s...", "INFO")
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            self.log("Interrupt received — shutting down", "WARNING")
        finally:
            self.state.is_running = False
            self.log("Agent stopped", "INFO")
            self._print_session_summary()

    # -- Reporting --

    def _print_session_summary(self):
        duration = ""
        if self.state.session_start:
            dur = datetime.now() - self.state.session_start
            minutes = int(dur.total_seconds() // 60)
            duration = f" ({minutes} min)"

        print(f"\n{'='*60}")
        print(f"  SESSION SUMMARY{duration}")
        print(f"{'='*60}")
        print(f"  Total Trades   : {self.state.total_trades}")
        print(f"  Wins           : {self.state.winning_trades}")
        print(f"  Losses         : {self.state.losing_trades}")
        print(f"  Total PnL      : ${self.state.total_pnl:.2f}")
        print(f"  Best Trade     : ${self.state.best_trade_pnl:.2f}")
        print(f"  Worst Trade    : ${self.state.worst_trade_pnl:.2f}")
        if self.state.total_trades > 0:
            wr = (self.state.winning_trades / self.state.total_trades) * 100
            print(f"  Win Rate       : {wr:.1f}%")
        if self.state.active_strategy:
            print(f"  Last Strategy  : {self.state.active_strategy}")
        print(f"{'='*60}\n")

    def get_status(self) -> Dict:
        position = self.client.get_position("BTC")
        user_state = self.client.get_user_state()
        equity = 0
        account_mode = "unknown"
        if user_state:
            equity = float(user_state.get("effective_equity", 0))
            account_mode = user_state.get("account_mode", "unknown")

        return {
            "is_running": self.state.is_running,
            "network": self.config.network,
            "account_mode": account_mode,
            "account_equity": equity,
            "current_position": position,
            "active_strategy": self.state.active_strategy,
            "total_trades": self.state.total_trades,
            "total_pnl": self.state.total_pnl,
            "daily_pnl": self.state.daily_pnl,
            "timestamp": datetime.now().isoformat(),
        }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    print(f"\n{'='*60}")
    print("  HYPERLIQUID BTC MULTI-STRATEGY SCALPING AGENT")
    print(f"{'='*60}")
    print("  Strategies:")
    print("    1. Momentum Scalp")
    print("    2. Mean Reversion")
    print("    3. Volatility Squeeze Breakout")
    print("    4. Order Flow Imbalance")
    print("    5. Multi-Timeframe Confluence")
    print("    6. Funding Rate Fade")
    print("    7. Liquidity Sweep / BOS")
    print(f"{'='*60}\n")

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set. Copy .env-example to .env and configure.")
        return

    if not os.getenv("HYPERLIQUID_PRIVATE_KEY"):
        print("Warning: HYPERLIQUID_PRIVATE_KEY not set — read-only mode (no trading)")

    agent = BTCScalpingAgent(model_name="gpt-5.2", temperature=0.1, verbose=True)

    status = agent.get_status()
    print(f"  Network      : {status['network']}")
    print(f"  Account Mode : {status.get('account_mode', 'unknown')}")
    print(f"  Equity       : ${status['account_equity']:.2f}")
    if status.get('account_mode') == 'unified':
        print(f"    (Spot USDC used as perps margin in unified mode)")
    print(f"  Position     : {status['current_position'] or 'None'}")

    if status['account_equity'] == 0:
        print(f"\n  WARNING: No funds available. Deposit USDC to your Hyperliquid account.")

    print(f"\n  Press Ctrl+C to stop\n")

    agent.run_continuous(interval_seconds=30, max_cycles=None)


if __name__ == "__main__":
    main()
