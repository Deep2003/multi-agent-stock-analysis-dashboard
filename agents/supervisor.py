from datetime import datetime
import re
import json
import statistics
from langchain_core.messages import AIMessage
from state import AgentState, FinalReport
from agents.base import llm, clear_agent_logs, log_agent_execution, invoke_with_retry

# ---------------------------------------------------------------------------
# Expanded company-name → ticker lookup (no LLM needed for ticker extraction)
# ---------------------------------------------------------------------------
_TICKER_DICT = {
    # Big Tech
    "APPLE": "AAPL", "MICROSOFT": "MSFT", "GOOGLE": "GOOGL", "ALPHABET": "GOOGL",
    "AMAZON": "AMZN", "NVIDIA": "NVDA", "TESLA": "TSLA", "META": "META",
    "FACEBOOK": "META", "NETFLIX": "NFLX", "ADOBE": "ADBE", "SALESFORCE": "CRM",
    "ORACLE": "ORCL", "INTEL": "INTC", "AMD": "AMD", "QUALCOMM": "QCOM",
    "BROADCOM": "AVGO", "CISCO": "CSCO", "IBM": "IBM", "SAP": "SAP",
    # Finance
    "JPMORGAN": "JPM", "MORGAN": "MS", "GOLDMAN": "GS", "BANKOFAMERICA": "BAC",
    "WELLSFARGO": "WFC", "CITIGROUP": "C", "VISA": "V", "MASTERCARD": "MA",
    "PAYPAL": "PYPL", "BLACKROCK": "BLK", "BERKSHIRE": "BRK-B",
    # Healthcare / Pharma
    "JOHNSON": "JNJ", "PFIZER": "PFE", "MODERNA": "MRNA", "UNITEDHEALTH": "UNH",
    "ABBVIE": "ABBV", "ELI": "LLY", "LILLY": "LLY", "MERCK": "MRK",
    # Consumer / Retail
    "WALMART": "WMT", "TARGET": "TGT", "COSTCO": "COST", "MCDONALDS": "MCD",
    "STARBUCKS": "SBUX", "NIKE": "NKE", "DISNEY": "DIS", "COMCAST": "CMCSA",
    # Energy
    "EXXON": "XOM", "CHEVRON": "CVX", "CONOCOPHILLIPS": "COP",
    # Semiconductors / Cloud
    "MICRON": "MU", "APPLIED": "AMAT", "LAM": "LRCX", "ASML": "ASML",
    "SNOWFLAKE": "SNOW", "PALANTIR": "PLTR", "SERVICENOW": "NOW",
    "CLOUDFLARE": "NET", "DATADOG": "DDOG", "MONGODB": "MDB",
    "CROWDSTRIKE": "CRWD", "PALO": "PANW", "FORTINET": "FTNT",
    "UBER": "UBER", "LYFT": "LYFT", "AIRBNB": "ABNB", "SHOPIFY": "SHOP",
    "SQUARE": "SQ", "BLOCK": "SQ", "COINBASE": "COIN", "ROBINHOOD": "HOOD",
    "SPOTIFY": "SPOT", "SNAP": "SNAP", "TWITTER": "TWTR", "PINTEREST": "PINS",
    "ZOOM": "ZM", "SLACK": "WORK", "ATLASSIAN": "TEAM", "HUBSPOT": "HUBS",
    # Autos
    "GM": "GM", "FORD": "F", "RIVIAN": "RIVN", "LUCID": "LCID",
    # ETFs / Index (pass-through)
    "SPY": "SPY", "QQQ": "QQQ", "IWM": "IWM", "DIA": "DIA", "XLK": "XLK",
}

# Stop-words that are NOT tickers even if all-caps in queries
_STOP_WORDS = {
    "I", "A", "AN", "THE", "AND", "FOR", "TO", "IN", "OF", "ON", "AT", "BY",
    "OR", "IS", "IT", "AS", "BE", "DO", "GO", "UP", "IF", "SO", "NO", "MY",
    "WE", "US", "ME", "HE", "SHE", "STOCK", "NEWS", "ANALYZE", "ANALYSIS",
    "REPORT", "WHAT", "HOW", "WHY", "WHEN", "WITH", "FROM", "ABOUT",
    "PRICE", "TARGET", "BUY", "SELL", "HOLD", "SHARE", "SHARES", "INVEST",
}


def _extract_ticker(query: str) -> str:
    """Zero-LLM ticker extraction: dict lookup then uppercase regex fallback."""
    q_upper = query.upper()

    # 1. Check if any known company name (multi-word or single) is in the query
    for name, tick in _TICKER_DICT.items():
        if name in q_upper:
            return tick

    # 2. Extract uppercase tokens that look like tickers (1-5 uppercase letters)
    uppercase_tokens = re.findall(r"\b[A-Z]{1,5}\b", q_upper)
    candidates = [t for t in uppercase_tokens if t not in _STOP_WORDS]
    if candidates:
        return candidates[0]

    # 3. Capitalised words fallback — treat any word as a potential company name
    words = re.findall(r"\b[A-Za-z]{2,15}\b", query)
    filtered = [w.upper() for w in words if w.upper() not in _STOP_WORDS]
    if filtered:
        # Map through dict in case it's a company name written in mixed case
        for w in filtered:
            if w in _TICKER_DICT:
                return _TICKER_DICT[w]
        return filtered[0]

    return "AAPL"  # absolute fallback


def supervisor_node(state: AgentState):
    """Supervisor Node: Extracts ticker via pure regex/dict (zero LLM tokens)."""
    clear_agent_logs()

    user_query = state["messages"][-1].content
    ticker = _extract_ticker(user_query)

    log_msg = f"[Supervisor]: Extracted ticker '{ticker}' from query. Coordinating committee experts..."
    log_agent_execution("supervisor_ticker_extractor", "regex+dict", user_query, {"extracted_ticker": ticker})

    return {
        "ticker": ticker,
        "active_agent": "pre_fetch",
        "messages": [AIMessage(content=log_msg, name="Supervisor")]
    }


def _parse_price(s: str) -> float | None:
    """Extract the first float from a price-target string like '$135.00' or '135'."""
    if not s:
        return None
    m = re.search(r"([0-9]+(?:\.[0-9]+)?)", str(s).replace(",", ""))
    try:
        return float(m.group(1)) if m else None
    except Exception:
        return None


def _cap(text: str, max_chars: int) -> str:
    """Hard-cap a text string to max_chars, appending '...' if truncated."""
    if not text:
        return text
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."


def synthesis_node(state: AgentState):
    """Synthesis Node: Consolidates 5 expert reports into a final thesis.
    
    Key efficiency improvements:
    - Computes implied_movement_pct deterministically (no LLM math)
    - Computes consensus price target as median of expert targets (no LLM)
    - Caps each expert section at 400 chars to reduce input tokens
    - Uses plain-text + JSON extraction (no with_structured_output double-call)
    """
    ticker = state["ticker"]
    expert_reports = state.get("expert_reports", {})

    # ── Deterministic price extraction ──────────────────────────────────────
    financial_raw = state.get("financial_data", "")
    current_price = 0.0
    if financial_raw:
        price_match = re.search(r"Current Price:\s*\$([0-9\.]+)", financial_raw)
        if price_match:
            try:
                current_price = float(price_match.group(1))
            except Exception:
                pass

    # ── Deterministic consensus price target (median of expert targets) ──────
    raw_targets = []
    for expert, report in expert_reports.items():
        if expert == "risk":
            continue
        val = _parse_price(report.get("price_target", ""))
        if val and val > 0:
            raw_targets.append(val)

    if raw_targets:
        consensus_price_target = round(statistics.median(raw_targets), 2)
    else:
        consensus_price_target = 0.0

    # ── Deterministic implied movement ───────────────────────────────────────
    if current_price > 0 and consensus_price_target > 0:
        implied_movement_pct = round(
            ((consensus_price_target - current_price) / current_price) * 100, 2
        )
    else:
        implied_movement_pct = 0.0

    current_date_str = datetime.now().strftime("%B %d, %Y")

    # ── Build condensed expert blocks (capped at 400 chars each section) ─────
    expert_blocks = []
    for expert, report in expert_reports.items():
        if expert == "risk":
            expert_blocks.append(
                f"### RISK AUDIT\n"
                f"- Stance: {report.get('risk_recommendation')}\n"
                f"- Analysis: {_cap(report.get('risk_analysis', 'N/A'), 400)}\n"
                f"- Critiques: {json.dumps(report.get('audit_log', []))}"
            )
        else:
            expert_blocks.append(
                f"### {expert.upper()} EXPERT\n"
                f"- Rec: {report.get('recommendation')} | Target: {report.get('price_target')}\n"
                f"- Core: {_cap(report.get('core_analysis', 'N/A'), 400)}\n"
                f"- Bull: {_cap(report.get('bull_case', 'N/A'), 200)}\n"
                f"- Bear: {_cap(report.get('bear_case', 'N/A'), 200)}"
            )
    expert_details = "\n\n".join(expert_blocks)

    system_prompt = (
        f"You are the Lead Investment Supervisor. Synthesize the expert committee reports into a final "
        f"premium markdown investment thesis for {ticker.upper()}. Today: {current_date_str}.\n\n"
        f"PRE-COMPUTED NUMBERS (use these exactly — do NOT recalculate):\n"
        f"- Current Price: ${current_price:.2f}\n"
        f"- Committee Consensus Price Target: ${consensus_price_target:.2f}\n"
        f"- Implied Movement: {implied_movement_pct:+.2f}%\n\n"
        f"EXPERT COMMITTEE SUBMISSIONS:\n{expert_details}\n\n"
        f"MANDATE: Audit for temporal coherence ({current_date_str}). Override any anachronisms inline.\n"
        f"FACTUAL RULE: Only use numbers explicitly stated in expert submissions or pre-computed above. "
        f"Never invent prices, EPS, P/E, revenue, or margins.\n\n"
        f"Output a JSON object with exactly these keys:\n"
        f"  current_price (float), price_target (float), implied_movement_pct (float), executive_summary (string)\n"
        f"The executive_summary MUST be a rich markdown report using this structure:\n"
        f"# 🏛️ Institutional Investment Committee Consensus Thesis: {ticker.upper()}\n"
        f"## 📊 Executive Summary & Key Thesis Takeaways\n"
        f"> [!NOTE]\n> High-level overview.\n"
        f"- **Core Finding 1**: [primary driver from financials or product moat]\n"
        f"- **Core Finding 2**: [main growth catalyst or macro tailwind]\n"
        f"- **Core Finding 3**: [key risk concern]\n\n"
        f"## 🎯 Committee Consensus Recommendation: [BUY/HOLD/SELL/STRONG BUY/STRONG SELL]\n"
        f"> [!IMPORTANT]\n> **Consensus**: 2-3 sentence justification.\n\n"
        f"### 📊 Domain Stance Matrix\n"
        f"| Committee Domain | Stance | Target |\n| :--- | :---: | :---: |\n"
        f"| 💵 Financial | [rec] | [target] |\n"
        f"| 🛡️ Tech & Moat | [rec] | [target] |\n"
        f"| 📢 Sentiment | [rec] | N/A |\n"
        f"| 🌐 Macro | [rec] | N/A |\n"
        f"| ⚠️ Risk | [rec] | N/A |\n\n"
        f"---\n\n"
        f"## 💵 Financial Expert Audit\n- **Revenue & Margins**: ...\n- **Valuation**: ...\n- **Momentum**: ...\n\n"
        f"## 🛡️ Technology Moat & Product Pipeline\n- **Moat**: ...\n- **Roadmap**: ...\n- **Feasibility**: ...\n\n"
        f"## 🌐 Macro & Sector Benchmarks\n- **Macro Sentiment**: ...\n- **Tailwinds vs Headwinds**: ...\n\n"
        f"## 📢 Sentiment & Media Narrative\n- **Narrative Trajectory**: ...\n- **Media Momentum**: ...\n\n"
        f"## ⚠️ Adversarial Risk & Auditor Review\n- **Volatility & Implied Risk**: ...\n- **Critique Resolutions**: ...\n\n"
        f"Return ONLY the raw JSON object, no markdown code fences or extra text."
    )

    messages = [{"role": "system", "content": system_prompt}]

    # Plain-text invocation (no with_structured_output — avoids double-call on failure)
    res_current_price = current_price
    res_price_target = consensus_price_target
    res_implied_movement = implied_movement_pct
    res_summary = ""

    try:
        response = invoke_with_retry(llm, messages, agent_name="supervisor")
        text = response.content.strip()
        # Strip any accidental markdown code fences
        json_text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        json_text = re.sub(r"\s*```$", "", json_text).strip()
        parsed = json.loads(json_text)
        # Use LLM-generated summary prose but our own pre-computed numbers
        res_summary = parsed.get("executive_summary", "")
        # Accept LLM's price/target only if they're non-zero; our computed values are authoritative
        llm_price = float(parsed.get("current_price", 0) or 0)
        llm_target = float(parsed.get("price_target", 0) or 0)
        if llm_price > 0:
            res_current_price = llm_price
        if llm_target > 0:
            res_price_target = llm_target
        # Always recompute implied movement deterministically
        if res_current_price > 0 and res_price_target > 0:
            res_implied_movement = round(
                ((res_price_target - res_current_price) / res_current_price) * 100, 2
            )
    except Exception as e:
        print(f"[*] Synthesis JSON parse failed: {e}. Building from expert data.")
        # Hard fallback: build a minimal but correct summary from what we have
        recs = [r.get("recommendation", "Hold") for k, r in expert_reports.items() if k != "risk"]
        rec_counts = {}
        for r in recs:
            rec_counts[r] = rec_counts.get(r, 0) + 1
        top_rec = max(rec_counts, key=rec_counts.get) if rec_counts else "Hold"

        res_summary = (
            f"# 🏛️ Institutional Investment Committee Consensus Thesis: {ticker.upper()}\n\n"
            f"## 📊 Executive Summary\n"
            f"- Committee Consensus: **{top_rec}**\n"
            f"- Current Price: **${res_current_price:.2f}**\n"
            f"- Consensus Price Target: **${res_price_target:.2f}** ({res_implied_movement:+.2f}%)\n\n"
            f"## ⚠️ Note\nFull synthesis unavailable due to model error. See individual expert reports above.\n"
        )

    log_agent_execution(
        "supervisor_thesis_synthesis",
        system_prompt,
        "Consolidate expert reports into final markdown thesis.",
        {
            "current_price": res_current_price,
            "price_target": res_price_target,
            "implied_movement_pct": res_implied_movement,
            "executive_summary": res_summary[:500]
        }
    )

    return {
        "messages": [AIMessage(content=res_summary, name="Supervisor")],
        "current_price": res_current_price,
        "price_target": res_price_target,
        "implied_movement_pct": res_implied_movement,
        "active_agent": "finish"
    }
