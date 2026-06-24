from datetime import datetime
from langchain_core.messages import AIMessage
from state import AgentState
from agents.base import get_expert_report, _cap

def macro_node(state: AgentState):
    """Expert Node: Macro & Industry Expert.
    Ingests macro sector returns and index benchmarks. Handles peer audit and cross-talk revision loops.
    Supports dynamic web search tool-calling for deep context.
    """
    ticker = state["ticker"]
    raw_data = state["macro_data"]
    industry_metrics = state.get("industry_metrics", "No industry metrics available.")
    
    # Check for peer-review critiques & cross-talk instructions targeted at this specific expert
    risk_report = state.get("expert_reports", {}).get("risk", {})
    critiques = risk_report.get("audit_log", []) if isinstance(risk_report, dict) else []
    cross_talks = risk_report.get("cross_talk_log", []) if isinstance(risk_report, dict) else []
    
    my_critique = next((c for c in critiques if c.get("target_expert") == "macro"), None)
    my_cross_talk = next((c for c in cross_talks if c.get("target_expert") == "macro"), None)
    
    current_date_str = datetime.now().strftime("%B %d, %Y")
    
    system_prompt = (
        f"You are the Macro & Industry Expert on our institutional investment committee. Today: {current_date_str}.\n"
        f"Benchmark sector performance (SPY, QQQ, XLK) against index trends and macro conditions.\n"
        f"INDUSTRY PEER ANALYSIS: Compare the company's leverage and valuation multiples against sector-level "
        f"fundamentals in industry_metrics. State clearly whether it trades at a premium or discount to peers, "
        f"and whether its Debt-to-Equity is typical for its industry group.\n"
        f"Use only numbers from the pre-fetched data. Do not invent macro figures or peer comparisons."
    )
    
    user_prompt = (
        f"Pre-fetched macro indicators for {ticker.upper()}:\n{_cap(raw_data, 300)}\n\n"
        f"Pre-fetched sector/industry fundamentals for {ticker.upper()}:\n{_cap(industry_metrics, 300)}"
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
    
    report, loop_msgs = get_expert_report("macro", system_prompt, messages_payload, api_key=state.get("api_key"), selected_model=state.get("selected_model", "auto"), request_id=state.get("request_id"))
    
    reports = dict(state.get("expert_reports", {}))
    reports["macro"] = report
    
    log_msg = f"[Macro Expert Report]: Completed macroeconomic industry baseline audit. Industry Recommendation: {report['recommendation']}"
    
    return {
        "messages": loop_msgs + [AIMessage(content=log_msg, name="macro")],
        "expert_reports": reports
    }
