from langchain_core.messages import AIMessage
from state import AgentState
from tools.prefetch import parallel_pre_fetch_institutional_data

def pre_fetch_node(state: AgentState):
    """Pre-Fetch Node: Concurrent backend data pre-loading for the committee experts."""
    ticker = state["ticker"]
    fetched = parallel_pre_fetch_institutional_data(ticker)
    
    log_msg = f"[Backend]: Pre-fetching ticker data... Concurrently fetched quantitative financials, profile sector metrics, narrative roadmaps, media narratives, macro indices, and volatility metrics for {ticker.upper()}."
    
    return {
        "financial_data": fetched["financial_data"],
        "company_profile": fetched["company_profile"],
        "roadmap_data": fetched["roadmap_data"],
        "sentiment_data": fetched["sentiment_data"],
        "news_baseline": fetched.get("news_baseline", fetched["sentiment_data"]),
        "macro_data": fetched["macro_data"],
        "risk_metrics": fetched["risk_metrics"],
        "industry_metrics": fetched.get("industry_metrics", ""),
        "analyst_ratings": fetched.get("analyst_ratings", ""),
        "expert_reports": {},
        "revision_count": 0,
        "active_agent": "financial", # Signal the frontend to spin up all 5 parallel experts
        "messages": [AIMessage(content=log_msg, name="Backend")]
    }
