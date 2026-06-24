from langchain_core.messages import SystemMessage, HumanMessage
from tools.technical_tools import fetch_technical_indicators
from agents.base import invoke_with_retry, llm

def technical_node(state):
    """Technical Analysis Expert Node: Analyzes RSI, MACD, Support/Resistance, and Chart Trends."""
    print("[technical] Invoking LLM (plain text mode)...")
    ticker = state.get("ticker", "UNKNOWN")
    
    # Check if there is a revision request for this specific expert from the risk auditor
    revision_req = state.get("expert_reports", {}).get("technical_revision_request")
    
    technical_data = fetch_technical_indicators(ticker)
    
    system_prompt = f"""You are a top-tier Quantitative Technical Analyst at an elite hedge fund.
Your task is to analyze the chart metrics, momentum indicators, and support/resistance levels for {ticker.upper()}.
You only care about price action, volume, and momentum. Ignore company fundamentals or news.

Technical Data:
{technical_data}

Provide a concise, extremely professional technical analysis report (max 250 words).
Focus on:
1. Momentum & Trend (RSI and MACD signals)
2. Volatility (Bollinger Bands)
3. Key Price Levels (Support floors and Resistance ceilings)
4. A final 1-sentence technical conviction (e.g., 'Bullish breakout setup', 'Oversold bounce expected', 'Bearish momentum accelerating').
Format clearly with bullet points."""

    messages = [SystemMessage(content=system_prompt)]
    if revision_req:
        messages.append(HumanMessage(content=f"Revision requested by Risk Auditor:\n{revision_req}\n\nPlease update your technical analysis to address these specific concerns."))
    else:
        messages.append(HumanMessage(content=f"Provide the technical analysis for {ticker}."))

    selected_model = state.get("selected_model", "auto")
    
    try:
        response = invoke_with_retry(llm, messages, agent_name="technical", selected_model=selected_model, request_id=state.get("request_id"))
        report_text = response.content
    except Exception as e:
        print(f"[*] Technical LLM failed: {e}")
        report_text = f"Technical analysis unavailable due to API error: {str(e)}"
    
    report_dict = {
        "core_analysis": report_text,
        "recommendation": "Hold", # Technical agent is pure price action, keeping default struct
        "price_target": "N/A"
    }
    
    return {
        "expert_reports": {"technical": report_dict}
    }
