from datetime import datetime
import re
import json
from langchain_core.messages import AIMessage
from state import AgentState, TickerExtraction, FinalReport
from agents.base import llm, clear_agent_logs, log_agent_execution, invoke_with_retry

def supervisor_node(state: AgentState):
    """Supervisor Node: Extracts ticker and triggers pre-fetch routing."""
    # Start of execution path: Clear all previous agent run logs
    clear_agent_logs()
    
    system_prompt = (
        "You are the Ticker Extraction Agent. Your ONLY job is to extract the stock ticker "
        "symbol from the user's query. Output it in uppercase. E.g. 'AAPL' for Apple, "
        "'TSLA' for Tesla. If no ticker is found, default to 'AAPL'."
    )
    
    structured_llm = llm.with_structured_output(TickerExtraction)
    user_query = state["messages"][-1].content
    
    COMMON_MAPPINGS = {
        "APPLE": "AAPL",
        "MICROSOFT": "MSFT",
        "GOOGLE": "GOOGL",
        "ALPHABET": "GOOGL",
        "AMAZON": "AMZN",
        "NVIDIA": "NVDA",
        "TESLA": "TSLA",
        "META": "META",
        "FACEBOOK": "META",
        "NETFLIX": "NFLX",
        "AMD": "AMD",
        "BROADCOM": "AVGO",
        "INTEL": "INTC",
        "QUALCOMM": "QCOM",
        "ADOBE": "ADBE",
        "SALESFORCE": "CRM",
        "ORACLE": "ORCL",
    }
    
    try:
        extraction = invoke_with_retry(structured_llm, [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ], max_retries=1, agent_name="supervisor")
        ticker = extraction.ticker.upper()
    except Exception as e:
        print(f"[*] Note: Ticker extraction structured output failed: {e}. Falling back to robust regex.")
        # Try to find an all-uppercase word first (excluding common words)
        uppercase_words = re.findall(r"\b[A-Z]{1,5}\b", user_query)
        filtered = [w for w in uppercase_words if w not in ["I", "A", "THE", "AND", "FOR", "TO", "IN", "OF", "ON", "AT", "BY"]]
        if filtered:
            ticker = filtered[0]
        else:
            words = re.findall(r"\b[A-Za-z]{2,15}\b", user_query)
            filtered_words = [w.upper() for w in words if w.upper() not in ["THE", "AND", "FOR", "TO", "IN", "OF", "ON", "AT", "BY", "STOCK", "NEWS", "ANALYZE"]]
            ticker = filtered_words[0] if filtered_words else "AAPL"
        
    ticker = ticker.upper()
    ticker = COMMON_MAPPINGS.get(ticker, ticker)
        
    log_msg = f"[Supervisor]: Extracted ticker symbol '{ticker}' from query. Coordinating committee experts..."
    
    # Log the inputs and outputs of the supervisor's ticker extraction
    log_agent_execution(
        "supervisor_ticker_extractor",
        system_prompt,
        user_query,
        {"extracted_ticker": ticker}
    )
    
    return {
        "ticker": ticker,
        "active_agent": "pre_fetch",
        "messages": [AIMessage(content=log_msg, name="Supervisor")]
    }


def synthesis_node(state: AgentState):
    """Synthesis Node: Consolidates the 5 expert reports into a final thesis with strict mathematical grounding."""
    ticker = state["ticker"]
    expert_reports = state.get("expert_reports", {})
    
    # Format the complete structured report details for synthesis reference
    expert_blocks = []
    for expert, report in expert_reports.items():
        if expert == "risk":
            expert_blocks.append(
                f"### {expert.upper()} EXPERT AUDIT (Auditor & Risk Stance)\n"
                f"- **Risk Stance/Recommendation**: {report.get('risk_recommendation')}\n\n"
                f"**Standalone Risk Analysis**:\n{report.get('risk_analysis')}\n\n"
                f"**Peer Critique Logs**:\n{json.dumps(report.get('audit_log', []), indent=2)}\n\n"
                f"**Supervisor Cross-Talk Logs**:\n{json.dumps(report.get('cross_talk_log', []), indent=2)}\n"
            )
        else:
            expert_blocks.append(
                f"### {expert.upper()} EXPERT AUDIT\n"
                f"- **Recommendation**: {report.get('recommendation')}\n"
                f"- **Estimated Price Target**: {report.get('price_target')}\n\n"
                f"**Core Analysis**:\n{report.get('core_analysis')}\n\n"
                f"**Bull Case scenario**:\n{report.get('bull_case')}\n\n"
                f"**Bear Case scenario**:\n{report.get('bear_case')}\n"
            )
    expert_details = "\n\n".join(expert_blocks)
    
    # Grounding current price from pre-fetched quantitative state
    financial_raw = state.get("financial_data", "")
    current_price = 0.0
    if financial_raw:
        price_match = re.search(r"Current Price:\s*\$([0-9\.]+)", financial_raw)
        if price_match:
            try:
                current_price = float(price_match.group(1))
            except Exception:
                pass

    current_date_str = datetime.now().strftime("%B %d, %Y")

    system_prompt = (
        "You are the Lead Investment Supervisor coordinating our institutional investment committee. "
        "Your task is to synthesize the five expert analysis reports (Financials, Moat & Innovation, Sentiment Narrative, "
        "Macro Benchmarks, and Risk Audit) into a final, premium-quality, highly polished structured markdown investment thesis.\n\n"
        f"FINAL AUDIT MANDATE: As the committee supervisor, you are responsible for absolute temporal coherence based on today's date: {current_date_str}. You must rigorously audit the reports from the Tech, Financial, and Sentiment nodes to ensure no historical anachronisms survive the final synthesis. If an expert describes a legacy product as a future pipeline or miscalculates market scale, explicitly override and correct the text to reflect reality as of {current_date_str}.\n\n"
        f"Expert Committee Submissions:\n{expert_details}\n\n"
        f"CRITICAL INSTRUCTION: You MUST extract the 'Current Price' directly from the provided `financial_data` state before calculating any upside or downside. Do not rely on your internal training data for stock prices. If your calculated Price Target is lower than the Current Price, you MUST describe it as a 'downside' or 'premium', and the percentage must be negative. Never call a lower price target an 'upside'.\n\n"
        f"Grounding Data Reference:\n"
        f"- Target Ticker: {ticker.upper()}\n"
        f"- Grounding Current Price: ${current_price:.2f}\n\n"
        f"You MUST structure the executive_summary report exactly as follows to ensure visual excellence and clear readability on our executive dashboard:\n\n"
        f"# 🏛️ Institutional Investment Committee Consensus Thesis: {ticker.upper()}\n\n"
        f"## 📊 Executive Summary & Key Thesis Takeaways\n"
        f"> [!NOTE]\n"
        f"> High-level overview of the target asset's current investment thesis and committee standing.\n"
        f"- **Core Finding 1**: [Summarize the primary driver from financials or product moat]\n"
        f"- **Core Finding 2**: [Summarize the main growth catalyst or macro tailwind]\n"
        f"- **Core Finding 3**: [Summarize the key auditor risk concern or regulatory bottleneck]\n\n"
        f"## 🎯 Committee Consensus Recommendation: [BUY | HOLD | SELL | STRONG BUY | STRONG SELL]\n"
        f"> [!IMPORTANT]\n"
        f"> **Consensus Target Stance**: Elaborate here on the joint target valuation or valuation multiplier and provide a 2-3 sentence absolute core consensus justification.\n\n"
        f"### 📊 Domain Stance Matrix\n"
        f"| Committee Domain | Recommendation Stance | Target Price / Impact Stance |\n"
        f"| :--- | :---: | :---: |\n"
        f"| 💵 Financial Health | [Rec Stance, e.g., Buy] | [Target Price, e.g., $150.00] |\n"
        f"| 🛡️ Moat & Technology | [Rec Stance] | [Valuation/roadmap Impact] |\n"
        f"| 📢 Sentiment Narrative | [Rec Stance] | N/A |\n"
        f"| 🌐 Macro & Industry | [Rec Stance] | N/A |\n"
        f"| ⚠️ Risk & Audit | [Rec Stance] | N/A |\n\n"
        f"---\n\n"
        f"## 💵 Financial Expert Audit\n"
        f"*Quantitative valuation, margin trends, balance sheet strength, and momentum cross-overs:*\n"
        f"- **Revenue & Margins**: [Provide a beautiful analysis here]\n"
        f"- **Valuation Assessment**: [Provide detailed financial ratios]\n"
        f"- **Financial Momentum**: [Provide SMA momentum analysis]\n\n"
        f"## 🛡️ Technology Moat & Product Pipeline Assessment\n"
        f"*Competitive moat, strategic R&D spend, and future product roadmap viability:*\n"
        f"- **Current Moat & Stack**: [Analyze scale and moat]\n"
        f"- **Roadmap Milestones**: [Analyze product roadmap pipeline]\n"
        f"- **Roadmap Innovation Feasibility**: [Analyze R&D conversion rate]\n\n"
        f"## 🌐 Macro & Sector Benchmarks\n"
        f"*Industry tailwinds, headwind concerns, and index relative strength:*\n"
        f"- **Macro Sector Sentiment**: [Analyze macro headwinds/tailwinds]\n"
        f"- **Tailwinds vs. Headwinds**: [Compare macro factors]\n\n"
        f"## 📢 Sentiment & Media Narrative\n"
        f"*News coverage volumes, investor sentiment, and executive earnings call narrative momentum:*\n"
        f"- **Narrative Trajectory**: [Analyze news search sentiments]\n"
        f"- **Media Momentum**: [Evaluate public and board narrative volume]\n\n"
        f"## ⚠️ Adversarial Risk & Auditor's Review\n"
        f"*Volatility, options implied risk, regulatory challenges, downside targets, and peer audit resolution:*\n"
        f"- **Volatility & Implied Risk**: [Analyze standalone downside risks]\n"
        f"- **Adversarial Critique Resolutions**: [Explain any peer challenges raised by Risk and how the experts resolved them]\n\n"
        f"Please output ONLY the formatted markdown report in the executive_summary field using appropriate bullet points, bold highlighting, clean formatting, and clear markdown tables. Do not wrap in extra conversational text or markdown code blocks."
        f"\n\nFACTUAL GROUNDING MANDATE: Before writing any number into the final report, you MUST verify it against the Grounding Current Price (${current_price:.2f}) and the expert committee submissions above. "
        f"Rules you must follow:\n"
        f"  1. NEVER invent or interpolate a stock price, revenue figure, EPS, P/E, market cap, or margin that is not explicitly provided in the expert submissions or the financial data.\n"
        f"  2. If an expert cited a number that contradicts the grounding data, use the grounding data and note the correction inline.\n"
        f"  3. All price targets in the Domain Stance Matrix must be real numbers pulled directly from the expert reports — do not fabricate them.\n"
        f"  4. The implied_movement_pct field you return must equal exactly ((price_target - {current_price:.2f}) / {current_price:.2f}) * 100 rounded to 2 decimal places."
    )
    
    messages = [{"role": "system", "content": system_prompt}] + list(state["messages"])
    
    structured_llm = llm.with_structured_output(FinalReport)
    
    report_obj = None
    try:
        report_obj = invoke_with_retry(structured_llm, messages, agent_name="supervisor")
    except Exception as e:
        print(f"[*] Note: Native structured output failed for Supervisor Synthesis: {e}. Activating fallback parser.")
        
    if report_obj:
        res_current_price = report_obj.current_price
        res_price_target = report_obj.price_target
        res_implied_movement = report_obj.implied_movement_pct
        res_summary = report_obj.executive_summary
    else:
        # Fallback regex-based parser
        fallback_prompt = (
            "You MUST return a JSON object with the exact keys: current_price, price_target, implied_movement_pct, executive_summary.\n"
            "Return ONLY the raw JSON block without markdown formatting or surrounding explanation."
        )
        fallback_messages = messages + [{"role": "user", "content": fallback_prompt}]
        try:
            response = invoke_with_retry(llm, fallback_messages, agent_name="supervisor")
            text = response.content.strip()
            # clean json markup if any
            json_text = re.sub(r"^```(json)?\s*", "", text, flags=re.IGNORECASE)
            json_text = re.sub(r"\s*```$", "", json_text)
            parsed = json.loads(json_text.strip())
            res_current_price = float(parsed.get("current_price", current_price))
            res_price_target = float(parsed.get("price_target", 0.0))
            res_implied_movement = float(parsed.get("implied_movement_pct", 0.0))
            res_summary = parsed.get("executive_summary", "")
        except Exception as err:
            print(f"[*] Note: Fallback JSON parsing failed for Supervisor Synthesis: {err}. Building manual placeholder.")
            # Manual fallback from the committee details
            res_current_price = current_price
            res_price_target = 0.0
            # Attempt to extract first numerical target from expert reports
            for expert, r in expert_reports.items():
                if expert != "risk" and "price_target" in r:
                    tgt_str = r.get("price_target", "")
                    num_match = re.search(r"([0-9\.]+)", tgt_str)
                    if num_match:
                        try:
                            res_price_target = float(num_match.group(1))
                            break
                        except Exception:
                            pass
            
            if res_price_target > 0 and res_current_price > 0:
                res_implied_movement = ((res_price_target - res_current_price) / res_current_price) * 100
            else:
                res_implied_movement = 0.0
                
            res_summary = (
                f"# 🏛️ Institutional Investment Committee Consensus Thesis: {ticker.upper()}\n\n"
                f"## 📊 Executive Summary & Key Thesis Takeaways\n"
                f"- Financial Health target price estimated at ${res_price_target:.2f} compared to live price ${res_current_price:.2f}.\n\n"
                f"## 💵 Financial Expert Audit\n"
                f"Committee Consensus Stance estimated price target at: ${res_price_target:.2f}.\n"
            )
            
    # Log supervisor thesis synthesis
    log_agent_execution(
        "supervisor_thesis_synthesis",
        system_prompt,
        "Consolidate all expert reports and critiques into the final structured markdown investment thesis with strict mathematical grounding.",
        {
            "current_price": res_current_price,
            "price_target": res_price_target,
            "implied_movement_pct": res_implied_movement,
            "executive_summary": res_summary
        }
    )
    
    return {
        "messages": [AIMessage(content=res_summary, name="Supervisor")],
        "current_price": res_current_price,
        "price_target": res_price_target,
        "implied_movement_pct": res_implied_movement,
        "active_agent": "finish"
    }
