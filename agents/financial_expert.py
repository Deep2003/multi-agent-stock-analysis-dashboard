from datetime import datetime
from langchain_core.messages import AIMessage
from state import AgentState
from agents.base import get_expert_report

def financial_node(state: AgentState):
    """Expert Node: Financial Expert.
    Ingests quantitative metrics and generates structured analysis. Handles peer audit and cross-talk revision loops.
    Supports dynamic web search tool-calling for deep context.
    """
    ticker = state["ticker"]
    raw_data = state["financial_data"]
    
    # Check for peer-review critiques & cross-talk instructions targeted at this specific expert
    risk_report = state.get("expert_reports", {}).get("risk", {})
    critiques = risk_report.get("audit_log", []) if isinstance(risk_report, dict) else []
    cross_talks = risk_report.get("cross_talk_log", []) if isinstance(risk_report, dict) else []
    
    my_critique = next((c for c in critiques if c.get("target_expert") == "financial"), None)
    my_cross_talk = next((c for c in cross_talks if c.get("target_expert") == "financial"), None)
    
    current_date_str = datetime.now().strftime("%B %d, %Y")
    
    system_prompt = (
        f"You are the Senior Financial Expert on our institutional investment committee.\n"
        f"Analyze the quantitative health, PE, growth, margins, and SMA crossover momentum of the stock.\n"
        f"VALUATION LOGIC CONSTRAINT: Today's exact date is {current_date_str}. Ground your analysis completely "
        f"in the current pricing climate. Cross-reference historical charts against major stock splits that occurred "
        f"prior to today (e.g., NVIDIA's 10-for-1 split in June 2024). Ensure your valuation logic treats split-adjusted "
        f"pricing correctly rather than framing a post-split price as an early-stage baseline.\n"
        f"Furthermore, when analyzing severe multiple compression (e.g., a trailing P/E dropping from 45x to a forward P/E "
        f"of 17x while the stock price remains high), you must attribute this correctly. Drastic multiple compression is driven "
        f"by massive expectations of top-line revenue and EPS explosions, NOT just minor gross margin expansions. Your qualitative "
        f"narrative must accurately reflect the mathematical realities of EPS growth required to compress that multiple.\n"
        f"TOOL ACCESS: You have been provided with baseline pre-fetched data in your context. Review this first. "
        f"If you need specific deep context or updated numbers not present in this baseline, you are authorized to invoke "
        f"the search tool (web_search). Do not abuse this permission; only query if the baseline is insufficient."
    )
    
    user_prompt = f"Pre-fetched financials for {ticker.upper()}:\n{raw_data}"
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
    
    report, loop_msgs = get_expert_report("financial", system_prompt, messages_payload)
    
    reports = dict(state.get("expert_reports", {}))
    reports["financial"] = report
    
    log_msg = f"[Financial Expert Report]: Completed Valuation & financial health audit. Estimated Target: {report['price_target']}"
    
    return {
        "messages": loop_msgs + [AIMessage(content=log_msg, name="financial")],
        "expert_reports": reports
    }
