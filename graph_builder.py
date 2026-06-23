from langgraph.graph import StateGraph, END
from state import AgentState
from agents.supervisor import supervisor_node, synthesis_node
from agents.prefetch import pre_fetch_node
from agents.financial_expert import financial_node
from agents.tech_expert import tech_product_node
from agents.sentiment_expert import sentiment_node
from agents.macro_expert import macro_node
from agents.risk_analyst import risk_node

def route_active_agent(state: AgentState):
    """Pristine linear router based on active_agent tracking."""
    active = state["active_agent"]
    if active == "finish":
        return END
    return active


def route_from_risk(state: AgentState):
    revision_count = state.get("revision_count", 0)
    risk_report = state.get("expert_reports", {}).get("risk", {})
    
    critiques = []
    if isinstance(risk_report, dict):
        critiques = risk_report.get("audit_log", [])
        
    if revision_count >= 2:
        # We reached our loop guard limit, route directly to synthesis!
        print(f"[Board Evaluation]: Max revision loops limit of 2 reached (Current: {revision_count}). Routing directly to Supervisor Synthesis...")
        return "synthesis"
        
    # Only HIGH severity critiques justify the cost of a full expert re-run.
    # Cross-talk items are passed to experts during revision but are NOT revision triggers on their own.
    flagged = []
    for c in critiques:
        target = c.get("target_expert")
        severity = c.get("severity", "Low").lower()
        if target in ["financial", "tech_product", "sentiment", "macro"] and severity == "high":
            flagged.append(target)
            
    flagged = list(set(flagged))
    if flagged:
        print(f"[Board Evaluation]: HIGH severity critiques detected (Revision Loop {revision_count}/2). Routing flagged experts for revision: {flagged}...")
        return flagged  # Return list of flagged node names to run concurrently in parallel!
        
    print("[Board Evaluation]: No HIGH severity critiques. Bypassing revision loop. Routing to synthesis...")
    return "synthesis"


workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("pre_fetch", pre_fetch_node)
workflow.add_node("financial", financial_node)
workflow.add_node("tech_product", tech_product_node)
workflow.add_node("sentiment", sentiment_node)
workflow.add_node("macro", macro_node)
workflow.add_node("risk", risk_node)
workflow.add_node("synthesis", synthesis_node)

# Edges
workflow.set_entry_point("supervisor")

workflow.add_edge("supervisor", "pre_fetch")

# Phase 1: Fork to the first 4 experts (Financial, Tech/Product, Sentiment, Macro)
workflow.add_edge("pre_fetch", "financial")
workflow.add_edge("pre_fetch", "tech_product")
workflow.add_edge("pre_fetch", "sentiment")
workflow.add_edge("pre_fetch", "macro")

# Phase 2: Fan-in to Risk Expert (Auditor)
workflow.add_edge("financial", "risk")
workflow.add_edge("tech_product", "risk")
workflow.add_edge("sentiment", "risk")
workflow.add_edge("macro", "risk")

# Phase 3 & 4: Conditional edge from risk node
workflow.add_conditional_edges(
    "risk",
    route_from_risk,
    {
        "financial": "financial",
        "tech_product": "tech_product",
        "sentiment": "sentiment",
        "macro": "macro",
        "synthesis": "synthesis"
    }
)

# Configure synthesis end
workflow.add_conditional_edges("synthesis", route_active_agent, {END: END})

# Compile graph
app = workflow.compile()
