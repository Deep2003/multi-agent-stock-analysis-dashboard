import urllib.parse
from duckduckgo_search import DDGS
from langchain_core.tools import tool
from tools.retry_utils import with_retry

import threading
import time

_search_lock = threading.Lock()

@tool
@with_retry(max_retries=3)
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo to retrieve news, recent earnings call highlights,
    R&D/roadmap progress, or comparative industry fundamentals. Use this tool if the baseline
    pre-fetched data is insufficient or you need specific updated context.
    """
    with _search_lock:
        time.sleep(1.0)
        try:
            with DDGS(timeout=10) as ddgs:
                results = list(ddgs.text(query, max_results=5))
                if not results:
                    return f"No search results found for query: '{query}'."
                formatted = []
                for r in results:
                    formatted.append(f"Title: {r.get('title')}\nSnippet: {r.get('body')}\nLink: {r.get('href')}")
                return "\n\n".join(formatted)
        except Exception as e:
            return "Search failed. Rely on your pre-fetched context."


@with_retry(max_retries=3)
def fetch_sentiment_news_data(ticker: str) -> str:
    """Lightweight DDG News baseline fetcher (replaces heavy Selenium scraper)."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(f"{ticker.upper()} stock financial news", max_results=10))
            if not results:
                return f"No news headlines could be retrieved for {ticker.upper()}."
            summary = f"Recent news headlines for {ticker.upper()} (fetched via DDG News):\n"
            for i, r in enumerate(results, 1):
                summary += f"{i}. {r.get('title')} (Source: {r.get('source')}, Date: {r.get('date')})\n"
            return summary
    except Exception as e:
        return f"Error fetching news narrative for {ticker}: {str(e)}"


@with_retry(max_retries=3)
def fetch_roadmap_data(ticker: str) -> str:
    """Programmatically pre-fetches future-facing product roadmaps, earnings call highlights,
    upcoming product lines, and R&D pipelines using targeted keyword search via DDG.
    Capped at 5 results with 150-char body snippets to minimise LLM input tokens.
    """
    try:
        query = f"{ticker.upper()} stock roadmap upcoming product pipeline earnings R&D next-generation"
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if not results:
                return f"No direct future roadmap press releases found for {ticker.upper()}."
            summary = f"--- Future Product Pipeline & R&D Indicators for {ticker.upper()} ---\n"
            headlines = []
            for r in results:
                body_snippet = (r.get('body') or '')[:150]
                headlines.append(f"- Headline: {r.get('title')}\n  Context: {body_snippet}\n  Link: {r.get('href')}")
            summary += "\n\n".join(headlines)
            return summary
    except Exception as e:
        return f"Error gathering product roadmap indicators: {str(e)}"

@with_retry(max_retries=3)
def fetch_reddit_sentiment(ticker: str) -> str:
    """Scrapes recent retail sentiment from Reddit investing communities via DDG."""
    try:
        query = f"{ticker.upper()} stock site:reddit.com/r/wallstreetbets OR site:reddit.com/r/stocks"
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if not results:
                return f"No recent Reddit discussions found for {ticker.upper()}."
            
            summary = [f"--- Retail Sentiment (Reddit) for {ticker.upper()} ---"]
            for r in results:
                title = r.get('title', '')
                body = (r.get('body') or '')[:150]
                summary.append(f"Title: {title}\nSnippet: {body}...\n")
            return "\n".join(summary)
    except Exception as e:
        return f"Error fetching Reddit sentiment for {ticker}: {str(e)}"
