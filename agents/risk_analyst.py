from datetime import datetime
from langchain_core.messages import AIMessage
from state import AgentState
from agents.base import get_risk_audit_report, _cap

def risk_node(state: AgentState):
    """Expert Node: Joint Board Evaluation & Dynamic Routing (The Cross-Talk Hub).
    Managed by the Supervisor Agent and the Risk Management Expert. Audits all 4 completed expert reports
    together to look for cross-domain dependencies, logical flaws, or compounding risks.
    """
    ticker = state["ticker"]
    risk_metrics = state["risk_metrics"]
    expert_reports = state.get("expert_reports", {})
    revision_count = state.get("revision_count", 0)
    
    # Gather reports of the other 4 experts
    financial_r = expert_reports.get("financial", {})
    tech_r = expert_reports.get("tech_product", {})
    sentiment_r = expert_reports.get("sentiment", {})
    macro_r = expert_reports.get("macro", {})
    
    # Cap core_analysis at 300 chars per expert — auditor needs enough to spot
    # factual errors and logical flaws, not the full essay (saves ~1,200 input tokens).
    peer_context = (
        "Here are the findings compiled by the other experts:\n\n"
        f"=== FINANCIAL EXPERT ===\n"
        f"Rec: {financial_r.get('recommendation', 'N/A')} | Target: {financial_r.get('price_target', 'N/A')}\n"
        f"Core: {_cap(financial_r.get('core_analysis', 'N/A'), 300)}\n\n"
        f"=== TECH & PRODUCT EXPERT ===\n"
        f"Rec: {tech_r.get('recommendation', 'N/A')} | Target: {tech_r.get('price_target', 'N/A')}\n"
        f"Core: {_cap(tech_r.get('core_analysis', 'N/A'), 300)}\n\n"
        f"=== SENTIMENT EXPERT ===\n"
        f"Rec: {sentiment_r.get('recommendation', 'N/A')}\n"
        f"Core: {_cap(sentiment_r.get('core_analysis', 'N/A'), 300)}\n\n"
        f"=== MACRO & INDUSTRY EXPERT ===\n"
        f"Rec: {macro_r.get('recommendation', 'N/A')}\n"
        f"Core: {_cap(macro_r.get('core_analysis', 'N/A'), 300)}\n"
    )
    
    current_date_str = datetime.now().strftime("%B %d, %Y")
    
    system_prompt = (
        f"You are the Risk & Audit Expert on our institutional investment committee. Today: {current_date_str}.\n"
        "ROLE: Internal auditor. Inspect all 4 expert reports for logical flaws, unbacked claims, and missing risks.\n\n"
        "SEVERITY RULES:\n"
        "  HIGH: ONLY hard factual errors — a number that directly contradicts pre-fetched ground truth. "
        "Fabricated analyst targets. Citing outdated chips as current. HIGH triggers expert re-run; use SPARINGLY.\n"
        "  MEDIUM: Framing issues, unsupported tone, missing risk factors. Logged but no re-run.\n"
        "  LOW: Minor stylistic issues. Logged, no action.\n\n"
        "FACTUAL AUDIT: Flag HIGH only if an expert cites a specific number (price, P/E, EPS, revenue, margin) "
        "that directly contradicts the pre-fetched data — not for rounding differences.\n"
        "Flag HIGH if an expert fabricates analyst price targets not in analyst_ratings.\n\n"
        "CROSS-TALK: Log cross-domain dependencies in cross_talk_log (informational only, no re-runs).\n\n"
        "STANDALONE RISK ANALYSIS: Assess volatility (Beta), short float %, regulatory threats, options implied risk."
    )
    
    financial_data = state.get("financial_data", "")
    analyst_ratings = state.get("analyst_ratings", "")
    
    user_prompt = (
        f"Pre-fetched Downside Risk & Volatility indicators for {ticker.upper()}:\n{risk_metrics}\n\n"
        f"Pre-fetched Quantitative Financials (GROUND TRUTH for Factual Integrity Audit):\n{financial_data}\n\n"
        f"Pre-fetched Wall Street Analyst Ratings (GROUND TRUTH for Factual Integrity Audit):\n{analyst_ratings}\n\n"
        f"=== PEER COMMITTEE SUBMISSIONS FOR JOINT BOARD AUDIT ===\n{peer_context}"
    )
    
    messages_payload = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Run the board evaluation/auditor invoker
    report = get_risk_audit_report(system_prompt, messages_payload, api_key=state.get("api_key"), selected_model=state.get("selected_model", "auto"))
    
    reports = dict(state.get("expert_reports", {}))
    reports["risk"] = report
    
    critiques = report.get("audit_log", [])
    cross_talks = report.get("cross_talk_log", [])
    
    active_agent = "synthesis"
    next_revision_count = revision_count
    
    # Only HIGH severity critiques justify the cost of a full expert re-run.
    # Cross-talk is preserved in state and passed to synthesis for context, but does NOT trigger re-runs.
    # Max 2 revision loops: first pass catches real errors, second confirms corrections.
    if revision_count < 2:
        high_severity_critiques = [
            c for c in critiques
            if c.get("target_expert") in ["financial", "tech_product", "sentiment", "macro"]
            and c.get("severity", "Low").lower() == "high"
        ]
        flagged = list(set(c.get("target_expert") for c in high_severity_critiques))
        if flagged:
            active_agent = ",".join(flagged)
            next_revision_count = revision_count + 1
            log_msg = f"[Board Evaluation]: Completed peer audit (Revision Loop {next_revision_count}/2). {len(high_severity_critiques)} HIGH severity critiques detected targeting: {flagged}. Triggering targeted revision..."
        else:
            medium_count = len([c for c in critiques if c.get("severity", "").lower() == "medium"])
            log_msg = f"[Board Evaluation]: Completed board audit. No HIGH severity critiques found ({medium_count} medium/low flagged — acceptable). Proceeding to synthesis."
    else:
        log_msg = f"[Board Evaluation]: Completed board audit. Maximum revision limit of 2 reached. Proceeding to final synthesis."
        
    return {
        "messages": [AIMessage(content=log_msg, name="risk")],
        "expert_reports": reports,
        "revision_count": next_revision_count,
        "active_agent": active_agent
    }
