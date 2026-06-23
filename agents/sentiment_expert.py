from datetime import datetime
from langchain_core.messages import AIMessage
from state import AgentState
from agents.base import get_expert_report

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
        f"You are the Media & Sentiment Expert on our institutional investment committee.\n"
        f"Analyze stock headlines and news topics to evaluate public retail narrative and sentiment.\n"
        f"MATERIALITY & RECENCY THRESHOLD: It is {current_date_str}. When scanning media and sentiment, "
        f"ignore all historical news prior to 2025. Furthermore, apply a scale filter: for mega-cap companies "
        f"(>$1 Trillion), ignore small-scale retail or ETF purchases (e.g., $50M - $100M trades) as they do not move "
        f"the needle. Focus only on massive institutional flow, hyperscaler capex announcements, and macro-level sentiment drivers "
        f"relevant to today.\n"
        f"WALL STREET CONSENSUS COMPARISON: You must evaluate the news and retail sentiment against the Wall Street analyst consensus ratings "
        f"and price targets provided in `analyst_ratings`. Explicitly identify if the media sentiment diverges from "
        f"the institutional consensus (e.g. news is highly bearish, but 80% of institutional analysts still maintain a Buy rating).\n"
        f"TOOL ACCESS: You have been provided with baseline pre-fetched data in your context. Review this first. "
        f"If you need specific deep context or updated numbers not present in this baseline, you are authorized to invoke "
        f"the search tool (web_search). Do not abuse this permission; only query if the baseline is insufficient."
    )
    
    user_prompt = (
        f"Pre-fetched news narrative for {ticker.upper()}:\n{raw_data}\n\n"
        f"Pre-fetched Wall Street consensus targets for {ticker.upper()}:\n{analyst_ratings}"
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
