import os
import re
import json
import datetime
import httpx
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from state import ExpertReport, RiskExpertOutput, TechExpertReport, MacroExpertReport, SentimentExpertReport

# Use explicit httpx.Timeout so that 'read' fires if the model stops streaming.
# We use a longer read/connect timeout (60s read, 15s connect) to allow large free
# models like LLaMA 3.3 70B sufficient time to queue and generate responses.
_http_timeout = httpx.Timeout(connect=15.0, read=60.0, write=60.0, pool=10.0)

def _create_llm(model_id: str, api_key: str = None):
    return ChatOpenAI(
        model=model_id,
        api_key=api_key or os.environ.get("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        temperature=0.0,
        timeout=_http_timeout,
        streaming=True,
        max_retries=0,
        default_headers={
            "HTTP-Referer": "https://github.com/langchain-ai/langchain",
            "X-Title": "LangChain Agentic Stock Analyst",
        }
    )

# Best active free models on OpenRouter with verified tool-calling support (validated 2026-06)
# Ordered by capability: largest/strongest first, smaller fallbacks after.
FREE_MODELS = [
    "meta-llama/llama-3.3-70b-instruct:free",       # Primary — strong reasoning, great tool use
    "google/gemma-4-31b-it:free",                   # Gemma 4 31B — extremely fast and capable
    "qwen/qwen3-next-80b-a3b-instruct:free",        # Qwen3 Next 80B — very strong
    "google/gemma-4-26b-a4b-it:free",               # Gemma 4 26B MoE
    "qwen/qwen3-coder:free",                        # Qwen3 Coder — excellent structure
    "openai/gpt-oss-120b:free",                     # GPT-OSS 120B
    "nousresearch/hermes-3-llama-3.1-405b:free",     # Hermes 3 Llama 3.1 405B — large fallback
    "cognitivecomputations/dolphin-mistral-24b-venice-edition:free", # Dolphin Mistral 24B
    "nvidia/nemotron-3-nano-30b-a3b:free",          # Nemotron 3 Nano 30B
    "openrouter/free",                              # OpenRouter Auto-router — last resort
]

llm = [_create_llm(m) for m in FREE_MODELS]

import time
import random
import threading
import queue
from langchain_core.callbacks import BaseCallbackHandler

class TokenStreamSubscriber:
    def __init__(self):
        self.q = queue.Queue()
    def put(self, val):
        self.q.put(val)

_subscribers_lock = threading.Lock()
_api_lock = threading.Lock()
active_subscribers = {}

def register_subscriber(request_id, sub):
    with _subscribers_lock:
        active_subscribers[request_id] = sub

def unregister_subscriber(request_id):
    with _subscribers_lock:
        active_subscribers.pop(request_id, None)

def publish_token(request_id, agent_name, token):
    if not request_id:
        return
    payload = {"event": "token", "agent": agent_name, "text": token}
    with _subscribers_lock:
        sub = active_subscribers.get(request_id)
        if sub:
            sub.put(payload)

class StreamingCallback(BaseCallbackHandler):
    def __init__(self, agent_name, request_id=None):
        self.agent_name = agent_name
        self.request_id = request_id
    def on_llm_new_token(self, token: str, **kwargs):
        publish_token(self.request_id, self.agent_name, token)

_request_lock = threading.Lock()
_last_request_time = 0.0

def invoke_with_retry(llm_inst, messages, max_retries=5, initial_delay=3.0, backoff_factor=2.0, agent_name=None, api_key=None, selected_model="auto", request_id=None):
    """Invokes the LLM instance with paced parallel execution (1.0s spacing)
    and exponential backoff with jitter to handle 429 and timeout errors.
    The httpx.Timeout on the LLM client (read=60s) is the primary hang-killer:
    if the model stops streaming for 60s, the connection is forcibly dropped.
    """
    global _last_request_time
    
    # 1. Pacing check under lock (does not block during the LLM call)
    sleep_time = 0.0
    with _request_lock:
        now = time.time()
        elapsed = now - _last_request_time
        if elapsed < 1.0:
            sleep_time = 1.0 - elapsed
            _last_request_time = now + sleep_time
        else:
            _last_request_time = now
            
    if sleep_time > 0:
        time.sleep(sleep_time)
        
    # 2. Invoke LLM with retry on rate limits and timeouts
    delay = initial_delay
    last_exception = None
    
    if selected_model and selected_model != "auto":
        # Build fallback list with selected model first, then all other FREE_MODELS
        unique_models = [selected_model]
        for m in FREE_MODELS:
            if m not in unique_models:
                unique_models.append(m)
        models_to_try = [_create_llm(m, api_key=api_key) for m in unique_models]
    elif api_key:
        models_to_try = [_create_llm(m, api_key=api_key) for m in FREE_MODELS]
    else:
        models_to_try = llm
    
    for attempt in range(max_retries):
        for current_llm in models_to_try:
            try:
                config = {}
                if agent_name:
                    config["callbacks"] = [StreamingCallback(agent_name, request_id)]
                
                if not api_key:
                    with _api_lock:
                        time.sleep(1) # Prevent rapid-fire concurrent requests on free tier
                        res = current_llm.invoke(messages, config=config)
                else:
                    res = current_llm.invoke(messages, config=config)
                    
                _last_request_time = time.time()
                return res
            except Exception as e:
                last_exception = e
                err_str = str(e)
                is_rate_limit = (
                    "too many requests" in err_str.lower() or
                    "429" in err_str or
                    "rate limit" in err_str.lower() or
                    "provider returned error" in err_str.lower() or
                    "limit exceeded" in err_str.lower()
                )
                is_timeout = (
                    "timed out" in err_str.lower() or
                    "timeout" in err_str.lower() or
                    "read timeout" in err_str.lower() or
                    isinstance(e, httpx.ReadTimeout) or
                    isinstance(e, httpx.ConnectTimeout)
                )
                is_unavailable = (
                    "404" in err_str or
                    "unavailable" in err_str.lower()
                )
                is_forbidden = (
                    "403" in err_str or
                    "401" in err_str or
                    "forbidden" in err_str.lower() or
                    "unauthorized" in err_str.lower()
                )
                
                # Treat ALL exceptions (including 500s, model overloaded, etc.) as retriable errors
                reason = "rate limit" if is_rate_limit else "timeout" if is_timeout else "forbidden" if is_forbidden else "unavailable" if is_unavailable else "model error"
                model_id = current_llm.model_name if hasattr(current_llm, 'model_name') else "Unknown Model"
                
                if current_llm != models_to_try[-1]:
                    print(f"[*] {reason.capitalize()} hit on {model_id} ({err_str[:60]}). Moving to fallback model instantly...")
                    continue
                else:
                    break # All fallbacks exhausted, trigger sleep and retry loop
                    
        # If we reach here, ALL models in the fallback chain failed for this attempt
        if attempt < max_retries - 1:
            jitter = random.uniform(0.8, 1.2)
            sleep_time = delay * jitter
            print(f"[*] All fallback models exhausted on attempt {attempt+1}/{max_retries}. Sleeping {sleep_time:.2f}s before retrying...")
            time.sleep(sleep_time)
            delay *= backoff_factor
            _last_request_time = time.time()
        else:
            raise last_exception




def normalize_recommendation(raw_rec: str) -> str:
    """Safely normalizes any recommendation string to one of the 5 strict Pydantic Literal values."""
    if isinstance(raw_rec, str):
        val = raw_rec.strip().lower()
        if "strong buy" in val:
            return "Strong Buy"
        if "strong sell" in val:
            return "Strong Sell"
        if "buy" in val:
            return "Buy"
        if "sell" in val:
            return "Sell"
        if "hold" in val:
            return "Hold"
    return "Hold"


def _cap(text: str, max_chars: int) -> str:
    """Hard-cap a text string to max_chars characters to control LLM input token cost."""
    if not text:
        return text or ""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."


def clear_agent_logs():
    """Clears the agent execution log file to prepare for a fresh analysis run."""
    log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agent_run_log.json")
    if os.path.exists(log_file):
        try:
            os.remove(log_file)
        except Exception:
            pass

def log_agent_execution(agent_name: str, system_prompt: str, user_prompt: str, output: any):
    """Logs the input prompts and output dicts/reports from each agent node to a shared JSON file."""
    log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agent_run_log.json")
    
    logs = []
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                logs = json.load(f)
        except Exception:
            logs = []
            
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "agent": agent_name,
        "inputs": {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt
        },
        "outputs": output
    }
    logs.append(log_entry)
    
    try:
        with open(log_file, "w") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"[*] Note: Failed to write agent log: {e}")

def run_tool_calling_loop(agent_name: str, messages: list) -> list:
    """Runs a loop allowing the LLM to call tools dynamically before finalizing the report.
    Returns the accumulated messages (both tool calls and tool responses).
    """
    # Skip costly sequential search loops. The pre-fetched data is already comprehensive.
    return messages

def _get_expert_report_raw(agent_name: str, system_prompt: str, messages: list, api_key: str = None, selected_model: str = "auto", request_id: str = None) -> dict:
    """Invokes the LLM using direct text completion + regex parsing.
    Bypasses with_structured_output entirely — function-calling hangs on free-tier models.
    Supports financial, tech_product, macro, and sentiment expert personas.
    """
    print(f"[{agent_name}] Invoking LLM (plain text mode)...")
        
    if agent_name == "tech_product":
        fallback_prompt = (
            "You MUST structure your response strictly with the following markdown headers:\n"
            "### Core Analysis\n"
            "(evaluation of current stack and market fit)\n"
            "### Future Product Roadmap\n"
            "Format upcoming product milestones here exactly like this (or leave empty if none):\n"
            "- **Product**: (product name)\n"
            "- **Timeline**: ( timeline like Q3 2026 )\n"
            "- **Feasibility**: High | Medium | Low\n"
            "- **Description**: (brief description of the milestone)\n"
            "### Innovation Risk\n"
            "(execution risk, delayed products assessment)\n"
            "### Bull Case\n"
            "(optimistic roadmap impact scenario)\n"
            "### Bear Case\n"
            "(pessimistic roadmap failure scenario)\n"
            "### Recommendation\n"
            "(Strong Buy | Buy | Hold | Sell | Strong Sell)\n"
            "### Price Target\n"
            "(estimated price target or N/A)\n\n"
            "Do not write any other conversational text or surrounding brackets."
        )
    elif agent_name == "macro":
        fallback_prompt = (
            "You MUST structure your response strictly with the following markdown headers:\n"
            "### Core Analysis\n"
            "(your findings on sector returns and index benchmarks)\n"
            "### Industry Comparison\n"
            "(comparison of company financials against industry metrics)\n"
            "### Bull Case\n"
            "(optimistic macro scenario)\n"
            "### Bear Case\n"
            "(pessimistic macro scenario)\n"
            "### Recommendation\n"
            "(Strong Buy | Buy | Hold | Sell | Strong Sell)\n"
            "### Price Target\n"
            "(estimated value or N/A)\n\n"
            "Do not write any other conversational text or surrounding brackets."
        )
    elif agent_name == "sentiment":
        fallback_prompt = (
            "You MUST structure your response strictly with the following markdown headers:\n"
            "### Core Analysis\n"
            "(your findings on retail and news sentiment)\n"
            "### Analyst Consensus\n"
            "(evaluation of news sentiment against Wall Street analyst consensus and targets)\n"
            "### Bull Case\n"
            "(optimistic sentiment scenario)\n"
            "### Bear Case\n"
            "(pessimistic sentiment scenario)\n"
            "### Recommendation\n"
            "(Strong Buy | Buy | Hold | Sell | Strong Sell)\n"
            "### Price Target\n"
            "(estimated value or N/A)\n\n"
            "Do not write any other conversational text or surrounding brackets."
        )
    else:
        fallback_prompt = (
            "You MUST structure your response strictly with the following markdown headers:\n"
            "### Core Analysis\n"
            "(your findings)\n"
            "### Bull Case\n"
            "(optimistic scenario)\n"
            "### Bear Case\n"
            "(pessimistic scenario)\n"
            "### Recommendation\n"
            "(Strong Buy | Buy | Hold | Sell | Strong Sell)\n"
            "### Price Target\n"
            "(estimated value or N/A)\n\n"
            "Do not write any other conversational text or surrounding brackets."
        )
        
    citation_rule = "\n\nCRITICAL RULE: You MUST explicitly cite the ORIGINAL source (e.g., the specific news outlet, SEC filing, or financial report, NOT the API) and the ORIGINAL publication/filing date for each piece of data, metric, news event, or claim you include in your analysis (e.g., 'Source: Bloomberg News, 2024-05-12'). Do not use the current date or access date as the citation.\n"
    fallback_messages = messages + [{"role": "user", "content": fallback_prompt + citation_rule}]
    last_err = None
    for attempt in range(3):
        try:
            response = invoke_with_retry(llm, fallback_messages, agent_name=agent_name, api_key=api_key, selected_model=selected_model, request_id=request_id)
            text = response.content.strip()
            
            def extract_section(section_name, content):
                pattern = rf"### {section_name}\s*(.*?)(?=###|$)"
                match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
                return match.group(1).strip() if match else "N/A"
                
            rec = extract_section("Recommendation", text)
            rec = normalize_recommendation(rec)
                
            if agent_name == "tech_product":
                roadmap = []
                roadmap_text = extract_section("Future Product Roadmap", text)
                items = re.split(r"-\s*\*\*Product\*\*:", roadmap_text)
                for item in items[1:]:
                    name_match = re.search(r"^\s*(.*?)\n", item)
                    timeline_match = re.search(r"-\s*\*\*Timeline\*\*:\s*(.*?)\n", item, re.IGNORECASE)
                    feasibility_match = re.search(r"-\s*\*\*Feasibility\*\*:\s*(High|Medium|Low)", item, re.IGNORECASE)
                    desc_match = re.search(r"-\s*\*\*Description\*\*:\s*(.*?)(?=- \*\*Product\*\*|- \*\*Timeline\*\*|- \*\*Feasibility\*\*|- \*\*Description\*\*|$)", item, re.DOTALL | re.IGNORECASE)
                    
                    name = name_match.group(1).strip() if name_match else "Upcoming Product"
                    timeline = timeline_match.group(1).strip() if timeline_match else "Q4 2026"
                    feasibility = feasibility_match.group(1).strip() if feasibility_match else "Medium"
                    
                    if not desc_match:
                        lines = [l.strip() for l in item.split("\n") if l.strip() and not any(k in l for k in ["**Timeline**", "**Feasibility**"])]
                        desc = " ".join(lines)
                    else:
                        desc = desc_match.group(1).strip()
                        
                    roadmap.append({
                        "product_name": name,
                        "timeline": timeline,
                        "feasibility": feasibility,
                        "description": desc
                    })
                    
                return {
                    "core_analysis": extract_section("Core Analysis", text),
                    "product_roadmap": roadmap,
                    "innovation_risk": extract_section("Innovation Risk", text),
                    "bull_case": extract_section("Bull Case", text),
                    "bear_case": extract_section("Bear Case", text),
                    "recommendation": rec,
                    "price_target": extract_section("Price Target", text)
                }
            elif agent_name == "macro":
                return {
                    "core_analysis": extract_section("Core Analysis", text),
                    "industry_comparison": extract_section("Industry Comparison", text),
                    "bull_case": extract_section("Bull Case", text),
                    "bear_case": extract_section("Bear Case", text),
                    "recommendation": rec,
                    "price_target": extract_section("Price Target", text)
                }
            elif agent_name == "sentiment":
                return {
                    "core_analysis": extract_section("Core Analysis", text),
                    "analyst_consensus": extract_section("Analyst Consensus", text),
                    "bull_case": extract_section("Bull Case", text),
                    "bear_case": extract_section("Bear Case", text),
                    "recommendation": rec,
                    "price_target": extract_section("Price Target", text)
                }
            else:
                return {
                    "core_analysis": extract_section("Core Analysis", text),
                    "bull_case": extract_section("Bull Case", text),
                    "bear_case": extract_section("Bear Case", text),
                    "recommendation": rec,
                    "price_target": extract_section("Price Target", text)
                }
        except Exception as err:
            last_err = err
            print(f"[*] {agent_name} failed to generate or parse valid report (attempt {attempt+1}/3): {err}. Retrying LLM prompt...")
            time.sleep(2)

    # If all 3 attempts fail, return a clean fallback without leaking technical tracebacks to the dashboard
    err_msg = "N/A - Analysis unavailable due to repeated API failures or model instability."
    if agent_name == "tech_product":
        return {
            "core_analysis": err_msg,
            "product_roadmap": [],
            "innovation_risk": "N/A",
            "bull_case": "N/A",
            "bear_case": "N/A",
            "recommendation": "Hold",
            "price_target": "N/A"
        }
    elif agent_name == "macro":
        return {
            "core_analysis": err_msg,
            "industry_comparison": "N/A",
            "bull_case": "N/A",
            "bear_case": "N/A",
            "recommendation": "Hold",
            "price_target": "N/A"
        }
    elif agent_name == "sentiment":
        return {
            "core_analysis": err_msg,
            "analyst_consensus": "N/A",
            "bull_case": "N/A",
            "bear_case": "N/A",
            "recommendation": "Hold",
            "price_target": "N/A"
        }
    else:
        return {
            "core_analysis": err_msg,
            "bull_case": "N/A",
            "bear_case": "N/A",
            "recommendation": "Hold",
            "price_target": "N/A"
        }

def get_expert_report(agent_name: str, system_prompt: str, messages: list, api_key: str = None, selected_model: str = "auto", request_id: str = None) -> tuple[dict, list]:
    """Wrapper that runs tool loop, fetches structured report, and logs agent execution.
    Returns a tuple of (report_dict, new_messages_from_loop).
    """
    # 1. Run the dynamic tool calling loop
    full_messages = run_tool_calling_loop(agent_name, messages)
    
    # new messages are the ones added after the initial system/user messages
    new_messages = full_messages[len(messages):]
    
    # 2. Get the structured report using the full message transcript
    report = _get_expert_report_raw(agent_name, system_prompt, full_messages, api_key=api_key, selected_model=selected_model, request_id=request_id)
    
    # Extract the user prompt from original messages
    user_prompt = ""
    if messages:
        last_msg = messages[-1]
        if isinstance(last_msg, dict):
            user_prompt = last_msg.get("content", "")
        else:
            user_prompt = getattr(last_msg, "content", str(last_msg))
            
    # Include tool results in logged user prompt for debugging/visibility
    tool_logs = ""
    for msg in new_messages:
        if isinstance(msg, ToolMessage):
            tool_logs += f"\n\n[TOOL RESULT - web_search]:\n{msg.content}"
    
    log_agent_execution(agent_name, system_prompt, user_prompt + tool_logs, report)
    return report, new_messages

def _get_risk_audit_report_raw(system_prompt: str, messages: list, api_key: str = None, selected_model: str = "auto", request_id: str = None) -> dict:
    """Invokes the LLM using direct text completion + regex parsing.
    Bypasses with_structured_output entirely — function-calling hangs on free-tier models.
    """
    print(f"[risk] Invoking LLM (plain text mode)...")
        
    fallback_prompt = (
        "You MUST structure your response strictly with the following markdown headers:\n"
        "### Standalone Risk Analysis\n"
        "(detailed risk findings on volatility, short interest, regulatory threats)\n"
        "### Risk Recommendation\n"
        "(Strong Buy | Buy | Hold | Sell | Strong Sell)\n"
        "### Audit Log\n"
        "If you want to critique other experts, list them here exactly like this (or leave empty if no critiques):\n"
        "- **Target**: financial | tech_product | sentiment | macro\n"
        "- **Severity**: High | Medium | Low\n"
        "- **Critique**: (detailed explanation of the flaw)\n\n"
        "### Cross-Talk Log\n"
        "If you want to link findings from one expert to another, list them here exactly like this (or leave empty if no cross-talk needed):\n"
        "- **Target**: financial | tech_product | sentiment | macro\n"
        "- **Source**: financial | tech_product | sentiment | macro\n"
        "- **Instruction**: (detailed instruction requesting this expert to ingest peer findings)\n\n"
        "Do not write any other conversational text or surrounding brackets."
    )
    
    fallback_messages = messages + [{"role": "user", "content": fallback_prompt}]
    try:
        response = invoke_with_retry(llm, fallback_messages, agent_name="risk", api_key=api_key, selected_model=selected_model, request_id=request_id)
        text = response.content.strip()
        
        def extract_section(section_name, content):
            pattern = rf"### {section_name}\s*(.*?)(?=###|$)"
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            return match.group(1).strip() if match else "N/A"
            
        rec = extract_section("Risk Recommendation", text)
        rec = normalize_recommendation(rec)
            
        audit_log = []
        audit_text = extract_section("Audit Log", text)
        items = re.split(r"-\s*\*\*Target\*\*:", audit_text)
        for item in items[1:]:
            target_match = re.search(r"^\s*(financial|tech_product|sentiment|macro)", item, re.IGNORECASE)
            severity_match = re.search(r"-\s*\*\*Severity\*\*:\s*(High|Medium|Low)", item, re.IGNORECASE)
            critique_match = re.search(r"-\s*\*\*Critique\*\*:\s*(.*?)(?=- \*\*Severity\*\*|- \*\*Critique\*\*|$)", item, re.DOTALL | re.IGNORECASE)
            
            if not critique_match:
                lines = [l.strip() for l in item.split("\n") if l.strip() and not l.startswith("- **Severity**")]
                critique = " ".join(lines)
            else:
                critique = critique_match.group(1).strip()
                
            target = target_match.group(1).lower().strip() if target_match else "financial"
            severity = severity_match.group(1).strip() if severity_match else "Medium"
            
            audit_log.append({
                "target_expert": target,
                "critique": critique,
                "severity": severity
            })
            
        cross_talk_log = []
        cross_talk_text = extract_section("Cross-Talk Log", text)
        ct_items = re.split(r"-\s*\*\*Target\*\*:", cross_talk_text)
        for item in ct_items[1:]:
            target_match = re.search(r"^\s*(financial|tech_product|sentiment|macro)", item, re.IGNORECASE)
            source_match = re.search(r"-\s*\*\*Source\*\*:\s*(financial|tech_product|sentiment|macro)", item, re.IGNORECASE)
            instruction_match = re.search(r"-\s*\*\*Instruction\*\*:\s*(.*?)(?=- \*\*Source\*\*|- \*\*Instruction\*\*|$)", item, re.DOTALL | re.IGNORECASE)
            
            if not instruction_match:
                lines = [l.strip() for l in item.split("\n") if l.strip() and not l.startswith("- **Source**")]
                instruction = " ".join(lines)
            else:
                instruction = instruction_match.group(1).strip()
                
            target = target_match.group(1).lower().strip() if target_match else "financial"
            source = source_match.group(1).lower().strip() if source_match else "tech_product"
            
            cross_talk_log.append({
                "target_expert": target,
                "instruction": instruction,
                "source_expert": source
            })
            
        return {
            "risk_analysis": extract_section("Standalone Risk Analysis", text),
            "risk_recommendation": rec,
            "audit_log": audit_log,
            "cross_talk_log": cross_talk_log
        }
    except Exception as err:
        return {
            "risk_analysis": f"Error parsing risk report data: {err}",
            "risk_recommendation": "Hold",
            "audit_log": [],
            "cross_talk_log": []
        }

def get_risk_audit_report(system_prompt: str, messages: list, api_key: str = None, selected_model: str = "auto", request_id: str = None) -> dict:
    """Wrapper that intercepts get_risk_audit_report calls, logging full inputs and outputs to a shared file."""
    report = _get_risk_audit_report_raw(system_prompt, messages, api_key=api_key, selected_model=selected_model, request_id=request_id)
    
    # Extract the user prompt from messages payload
    user_prompt = ""
    if messages:
        last_msg = messages[-1]
        if isinstance(last_msg, dict):
            user_prompt = last_msg.get("content", "")
        else:
            user_prompt = getattr(last_msg, "content", str(last_msg))
            
    log_agent_execution("risk_analyst", system_prompt, user_prompt, report)
    return report
