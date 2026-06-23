from datetime import datetime
from langchain_core.messages import AIMessage
from state import AgentState
from agents.base import get_expert_report, _cap

def sentiment_node(state: AgentState):
    """Expert Node: Media & Sentiment Expert.
    Evaluates headlines to compile overriding narrative sentiment. Handles peer audit and cross-talk revision loops.
    Supports dynamic web search tool-calling for deep context.
    """
    ticker = state["ticker"]
    raw_data = state.get("news_baseline", state.get("sentiment_data", "No news data available."))
    analyst_ratings = state.get("analyst_ratings", "No analyst ratings available.")
    
    # Check for peer-review critiques & cross-talk instructions targeted at this specific expert
    risk_report = state.get("expert_reports", {}).get("risk", {})
    critiques = risk_report.get("audit_log", []) if isinstance(risk_report, dict) else []
    cross_talks = risk_report.get("cross_talk_log", []) if isinstance(risk_report, dict) else []
    
    my_critique = next((c for c in critiques if c.get("target_expert") == "sentiment"), None)
    my_cross_talk = next((c for c in cross_talks if c.get("target_expert") == "sentiment"), None)
    
    current_date_str = datetime.now().strftime("%B %d, %Y")
    
    system_prompt = (
        f"You are the Media & Sentiment Expert on our institutional investment committee. Today: {current_date_str}.\n"
        f"Analyze headlines and news to evaluate public retail narrative and sentiment.\n"
        f"RECENCY FILTER: Ignore news prior to 2025. For mega-caps (>$1T), ignore small retail/ETF trades "
        f"(<$100M). Focus on institutional flows, hyperscaler capex, and macro-level sentiment drivers.\n"
        f"CONSENSUS DIVERGENCE: Compare news/retail sentiment against Wall Street analyst consensus in analyst_ratings. "
        f"Flag explicitly if media is bearish while institutions remain bullish (or vice versa).\n"
        f"Use only information from the pre-fetched data. Do not invent analyst targets or cite news you cannot see."
    )
    
    user_prompt = (
        f"Pre-fetched news narrative for {ticker.upper()}:\n{_cap(raw_data, 600)}\n\n"
        f"Pre-fetched Wall Street consensus for {ticker.upper()}:\n{_cap(analyst_ratings, 300)}"
    )
    
    if my_critique:
        user_prompt += f"\n\n[PEER AUDIT CRITIQUE - Severity: {my_critique['severity']}]\n"
        user_prompt += f"The Risk Management Expert has flagged your initial report with this critique:\n"
        user_prompt += f"'{my_critique['critique']}'\n"
        user_prompt += f"You MUST address this critique directly in your revised analysis. Include a clear explanation or Addendum clarifying your stance."
        
    if my_cross_talk:
        user_prompt += f"\n\n[CROSS-DOMAIN PEER CROSS-TALK INSTRUCTION]\n"
        user_prompt += f"The Joint Board has identified a cross-domain dependency. You must ingest the findings of the {my_cross_talk['source_expert'].upper()} Expert and address this instruction:\n"
        user_prompt += f"'{my_cross_talk['instruction']}'\n"
        
        peer_report = state.get("expert_reports", {}).get(my_cross_talk['source_expert'], {})
        user_prompt += f"\nHere is the {my_cross_talk['source_expert'].upper()} Expert's findings for reference:\n{peer_report.get('core_analysis', 'N/A')}\n"
        
    messages_payload = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    report, loop_msgs = get_expert_report("sentiment", system_prompt, messages_payload)
    
    reports = dict(state.get("expert_reports", {}))
    reports["sentiment"] = report
    
    log_msg = f"[Sentiment Expert Report]: Completed media narrative news audit. Sentiment Recommendation: {report['recommendation']}"
    
    return {
        "messages": loop_msgs + [AIMessage(content=log_msg, name="sentiment")],
        "expert_reports": reports
    }
