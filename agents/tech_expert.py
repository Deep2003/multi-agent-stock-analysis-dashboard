import re
from datetime import datetime
from langchain_core.messages import AIMessage
from state import AgentState
from agents.base import get_expert_report, _cap

def tech_product_node(state: AgentState):
    """Expert Node: Technology & Product Expert.
    Evaluates business moat scale, tech stack, and future product roadmap/R&D pipeline.
    Ingests peer audit and cross-talk revision loops.
    """
    ticker = state["ticker"]
    profile_data = state["company_profile"]
    roadmap_data = state.get("roadmap_data", "No future product roadmap data available.")
    
    current_date_str = datetime.now().strftime("%B %d, %Y")
    
    system_prompt = (
        f"You are the Technology & Product Expert on our institutional investment committee. Today: {current_date_str}.\n"
        f"Evaluate the company's tech moat, current stack, market fit, and forward-looking product roadmap/R&D pipeline.\n"
        f"HARDWARE TIMELINE: Anchor all analysis to the 2026 hardware cycle. For NVIDIA: Hopper=legacy, Blackwell=current, "
        f"Vera Rubin=next-gen. Benchmark only 2026-relevant competitors (AMD MI400/CDNA4, Google Trillium/TPU-v6).\n"
        f"Use only information from the pre-fetched data. Do not fabricate product timelines or specifications."
    )
    
    # Check for peer-review critiques & cross-talk instructions targeted at this specific expert
    risk_report = state.get("expert_reports", {}).get("risk", {})
    critiques = risk_report.get("audit_log", []) if isinstance(risk_report, dict) else []
    cross_talks = risk_report.get("cross_talk_log", []) if isinstance(risk_report, dict) else []
    
    my_critique = next((c for c in critiques if c.get("target_expert") == "tech_product"), None)
    my_cross_talk = next((c for c in cross_talks if c.get("target_expert") == "tech_product"), None)
    
    user_prompt = (
        f"Pre-fetched company profile/tech stack for {ticker.upper()}:\n{_cap(profile_data, 500)}\n\n"
        f"Pre-fetched product roadmap/R&D data for {ticker.upper()}:\n{_cap(roadmap_data, 1000)}"
    )
    
    if my_critique:
        user_prompt += f"\n\n[PEER AUDIT CRITIQUE - Severity: {my_critique['severity']}]\n"
        user_prompt += f"The Risk Management Expert has flagged your initial report with this critique:\n"
        user_prompt += f"'{my_critique['critique']}'\n"
        user_prompt += f"You MUST address this critique directly in your revised analysis. Include a clear explanation or Addendum."
        
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
    
    report, loop_msgs = get_expert_report("tech_product", system_prompt, messages_payload, api_key=state.get("api_key"), selected_model=state.get("selected_model", "auto"), request_id=state.get("request_id"))
    
    reports = dict(state.get("expert_reports", {}))
    reports["tech_product"] = report
    
    log_msg = f"[Product Expert Report]: Completed forward-looking tech stack & product roadmap audit. Moat Recommendation: {report['recommendation']}"
    
    return {
        "messages": loop_msgs + [AIMessage(content=log_msg, name="tech_product")],
        "expert_reports": reports
    }
