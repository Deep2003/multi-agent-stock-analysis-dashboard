from datetime import datetime
from langchain_core.messages import AIMessage
from state import AgentState
from agents.base import get_risk_audit_report

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
    
    peer_context = (
        "Here are the findings compiled by the other experts:\n\n"
        f"=== FINANCIAL EXPERT REPORT ===\n"
        f"Recommendation: {financial_r.get('recommendation', 'N/A')}\n"
        f"Price Target: {financial_r.get('price_target', 'N/A')}\n"
        f"Core Analysis: {financial_r.get('core_analysis', 'N/A')}\n\n"
        f"=== TECH & PRODUCT EXPERT REPORT ===\n"
        f"Recommendation: {tech_r.get('recommendation', 'N/A')}\n"
        f"Price Target: {tech_r.get('price_target', 'N/A')}\n"
        f"Core Analysis: {tech_r.get('core_analysis', 'N/A')}\n\n"
        f"=== SENTIMENT EXPERT REPORT ===\n"
        f"Recommendation: {sentiment_r.get('recommendation', 'N/A')}\n"
        f"Core Analysis: {sentiment_r.get('core_analysis', 'N/A')}\n\n"
        f"=== MACRO & INDUSTRY EXPERT REPORT ===\n"
        f"Recommendation: {macro_r.get('recommendation', 'N/A')}\n"
        f"Core Analysis: {macro_r.get('core_analysis', 'N/A')}\n"
    )
    
    current_date_str = datetime.now().strftime("%B %d, %Y")
    
    system_prompt = (
        "You are the Joint Board of our institutional investment committee, managed jointly by the Supervisor Agent and the Risk Management Expert.\n"
        f"Today's date is {current_date_str}.\n"
        "Your first job is to act as an internal auditor and cross-examiner. Inspect all 4 completed expert reports TOGETHER. "
        "Look for logical flaws, overly optimistic assumptions, unbacked claims, or missing risks. Log targeted critiques in audit_log.\n\n"
        "SEVERITY ESCALATION RULES — READ CAREFULLY:\n"
        "  - HIGH severity: ONLY for hard, verifiable factual errors. A number that directly contradicts the pre-fetched ground truth data. "
        "Fabricated analyst targets. Citing products/chips that are demonstrably outdated as 'current'. "
        "HIGH critiques trigger a full expert re-run, so use them SPARINGLY and only when CERTAIN.\n"
        "  - MEDIUM severity: Analytical framing issues, overly bullish/bearish tone without data support, missing risk factors. "
        "MEDIUM critiques are logged in the final report but do NOT trigger a re-run.\n"
        "  - LOW severity: Minor stylistic concerns, preference differences. Log these but do NOT flag them for revision.\n\n"
        "FACTUAL INTEGRITY AUDIT: Cross-examine quantitative claims in expert reports against the pre-fetched raw data. "
        "Flag HIGH only if an expert states a specific number (price, P/E, revenue, margin, EPS) that DIRECTLY CONTRADICTS the pre-fetched data block — "
        "not just because they rounded or estimated differently. "
        "Flag HIGH if an expert fabricates analyst price targets not present in the analyst_ratings block.\n\n"
        "AUDIT TRIPWIRES (HIGH severity only if clearly violated):\n"
        "  1. Tech Expert: Flag HIGH only if they explicitly cite Hopper/Blackwell as 'upcoming/future' when discussing current-gen chips.\n"
        "  2. Financial Expert: Flag HIGH only if they attribute drastic P/E multiple compression entirely to margin expansion, ignoring EPS/revenue growth math.\n\n"
        "CROSS-TALK: Identify cross-domain dependencies. Log them in cross_talk_log. These are informational \u2014 they do NOT trigger expert re-runs.\n\n"
        "Your final job is to compile your standalone risk analysis on market volatility, Beta, short float %, regulatory threats, and options pricing proxy."
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
    report = get_risk_audit_report(system_prompt, messages_payload)
    
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
