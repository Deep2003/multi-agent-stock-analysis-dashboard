import os
import sys
import json
import re
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage, AIMessage

# Local modular imports
from graph_builder import app
from frontend import HTML_FRONTEND_CONTENT
from agents.base import register_subscriber, unregister_subscriber, TokenStreamSubscriber
import asyncio
import time

# Retrieve configuration from base layer
model_name = os.environ.get("OPENROUTER_MODEL", "google/gemma-4-31b-it:free")

app_server = FastAPI(
    title="Agentic Stock Analyst Full-Stack Server",
    description="Web server hosting the multi-agent stock analysis system and serving an interactive React/Tailwind frontend."
)

app_server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app_server.get("/api/stream")
async def stream_analysis(query: str = Query(..., description="The stock query statement to analyze.")):
    """Server-Sent Events (SSE) streaming endpoint.
    Runs the LangGraph execution workflow and pushes live logs, metrics,
    state handoffs, and raw expert report Pydantic payloads back in real-time.
    """
    async def event_generator():
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "active_agent": "supervisor",
            "ticker": "",
            "financial_data": "",
            "company_profile": "",
            "roadmap_data": "",
            "sentiment_data": "",
            "news_baseline": "",
            "macro_data": "",
            "risk_metrics": "",
            "industry_metrics": "",
            "analyst_ratings": "",
            "expert_reports": {},
            "revision_count": 0,
            "current_price": 0.0,
            "price_target": 0.0,
            "implied_movement_pct": 0.0
        }
        
        yield f"data: {json.dumps({'event': 'start', 'message': 'Lead Supervisor parsing stock query...'})}\n\n"
        
        sub = TokenStreamSubscriber()
        register_subscriber(sub)
        
        async def run_graph():
            try:
                async for event in app.astream(initial_state, stream_mode="values"):
                    messages = event.get("messages", [])
                    if not messages:
                        continue
                    
                    last_msg = messages[-1]
                    
                    sender_val = getattr(last_msg, "name", None) or getattr(last_msg, "type", "System")
                    sender = str(sender_val).lower() if sender_val else "system"
                    
                    active_agent_val = event.get("active_agent", "") or ""
                    active_agent = str(active_agent_val).lower()
                    
                    financial_raw = event.get("financial_data", "")
                    
                    # Parse metrics dynamically to update stats card
                    metrics = {}
                    if financial_raw:
                        pe_match = re.search(r"Trailing P/E:\s*([0-9\.]+)", financial_raw)
                        mc_match = re.search(r"Market Cap:\s*\$([0-9,]+)", financial_raw)
                        eps_match = re.search(r"EPS \(Trailing\):\s*([0-9\.-]+)", financial_raw)
                        price_match = re.search(r"Current Price:\s*\$([0-9\.]+)", financial_raw)
                        sma50_match = re.search(r"50-Day SMA:\s*\$([0-9\.]+)", financial_raw)
                        
                        if pe_match: metrics["pe"] = pe_match.group(1)
                        if mc_match: metrics["market_cap"] = mc_match.group(1)
                        if eps_match: metrics["eps"] = eps_match.group(1)
                        if price_match: metrics["price"] = price_match.group(1)
                        if sma50_match: metrics["sma50"] = sma50_match.group(1)

                    payload = {
                        "event": "update",
                        "agent": sender,
                        "active_agent": active_agent,
                        "message": last_msg.content,
                        "ticker": event.get("ticker", ""),
                        "metrics": metrics,
                        "expert_reports": event.get("expert_reports", {}), # Push raw structured reports
                        "revision_count": event.get("revision_count", 0),  # Push revision count
                        "current_price": event.get("current_price", 0.0),
                        "price_target": event.get("price_target", 0.0),
                        "implied_movement_pct": event.get("implied_movement_pct", 0.0)
                    }
                    sub.put(payload)
                    
                sub.put({"event": "complete", "message": "Institutional committee analysis completed successfully!"})
            except Exception as e:
                sub.put({"event": "error", "message": str(e)})
            finally:
                sub.put(None)
                
        graph_task = asyncio.create_task(run_graph())
        deadline = time.monotonic() + 240  # 4-minute hard wall-clock limit
        
        try:
            while True:
                # Drain all available queue items to the client
                while not sub.q.empty():
                    item = sub.q.get_nowait()
                    if item is None:
                        return  # Sentinel: graph finished cleanly
                    yield f"data: {json.dumps(item)}\n\n"
                    
                # Exit if graph finished and queue is empty
                if graph_task.done() and sub.q.empty():
                    break
                
                # Enforce overall 4-minute deadline
                if time.monotonic() > deadline:
                    msg = "Analysis timed out after 4 minutes. The model may be overloaded — please retry."
                    yield f"data: {json.dumps({'event': 'error', 'message': msg})}\n\n"
                    graph_task.cancel()
                    break
                    
                await asyncio.sleep(0.05)
        finally:
            unregister_subscriber(sub)
            if not graph_task.done():
                graph_task.cancel()


    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app_server.get("/api/logs")
def get_agent_logs():
    """Returns the compiled agent execution logs file (agent_run_log.json) containing inputs and outputs."""
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent_run_log.json")
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Failed to read agent logs: {e}"}
    return []


@app_server.get("/", response_class=HTMLResponse)
def serve_frontend():
    """Serves the visually stunning 'Bloomberg meets modern SaaS' dark-mode web application."""
    # Replace the {model_name} tag dynamically to show current model configuration
    return HTML_FRONTEND_CONTENT.replace("{model_name}", model_name)


if __name__ == "__main__":
    # If the user wants traditional CLI execution, trigger the terminal stream
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        print("=" * 60)
        print("      HIGH-PERFORMANCE PRE-FETCH MULTI-AGENT SYSTEM (CLI)")
        print("=" * 60)
        
        if os.environ.get("OPENROUTER_API_KEY") == "placeholder_key" or not os.environ.get("OPENROUTER_API_KEY"):
            print("[!] Execution aborted: OPENROUTER_API_KEY is not configured.")
            sys.exit(1)
            
        ticker_input = "AAPL"
        query = f"Analyze the fundamentals and current sentiment for {ticker_input}."
        print(f"\nUser Query: '{query}'")
        print(f"LLM Backbone Model: '{model_name}'")
        print("\nRunning multi-agent analysis graph...")
        print("-" * 60)
        
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "active_agent": "supervisor",
            "ticker": "",
            "financial_data": "",
            "company_profile": "",
            "roadmap_data": "",
            "sentiment_data": "",
            "news_baseline": "",
            "macro_data": "",
            "risk_metrics": "",
            "industry_metrics": "",
            "analyst_ratings": "",
            "expert_reports": {},
            "revision_count": 0,
            "current_price": 0.0,
            "price_target": 0.0,
            "implied_movement_pct": 0.0
        }
        
        final_messages = []
        try:
            for event in app.stream(initial_state, stream_mode="values"):
                messages = event.get("messages", [])
                if messages:
                    final_messages = messages
                    last_msg = messages[-1]
                    sender = getattr(last_msg, "name", "System")
                    content_preview = last_msg.content[:150].replace("\n", " ")
                    if len(last_msg.content) > 150:
                        content_preview += "..."
                    print(f"[{sender or 'System'}] -> {content_preview}")
            
            print("-" * 60)
            print("\nFINAL SYNTHESIZED REPORT:\n")
            if final_messages:
                print(final_messages[-1].content)
        except Exception as e:
            print(f"\n[Error] Graph execution failed: {e}")
            sys.exit(1)
            
    else:
        # Default: Launch uvicorn web server serving the gorgeous browser dashboard
        import uvicorn
        print("=" * 65)
        print("   🚀 AGENTIC STOCK ANALYST FULL-STACK DASHBOARD IS ONLINE 🚀")
        print("=" * 65)
        print("   - High-performance programmatic parallel pre-fetching active.")
        print("   - Active LLM Backbone model:", model_name)
        print("   - Open your browser to access the premium dark-mode console:")
        print("     👉   http://localhost:8000")
        print("=" * 65)
        print("   * Note: To run the traditional CLI loop, execute with the flag:")
        print("     python stock_analyzer.py --cli")
        print("-" * 65)
        
        uvicorn.run(app_server, host="0.0.0.0", port=8000)
