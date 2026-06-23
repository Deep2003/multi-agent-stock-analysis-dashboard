import concurrent.futures
from tools.financial_tools import fetch_financial_data, fetch_company_profile, fetch_analyst_ratings
from tools.news_tools import fetch_roadmap_data, fetch_sentiment_news_data
from tools.macro_tools import fetch_macro_data, fetch_industry_metrics
from tools.risk_tools import fetch_risk_metrics

def parallel_pre_fetch_institutional_data(ticker: str) -> dict:
    """Executes the expanded programmatic pre-fetching concurrently across eight background threads."""
    print(f"[Backend]: Pre-fetching institutional data for {ticker.upper()}...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        f_financial = executor.submit(fetch_financial_data, ticker)
        f_profile = executor.submit(fetch_company_profile, ticker)
        f_roadmap = executor.submit(fetch_roadmap_data, ticker)
        f_sentiment = executor.submit(fetch_sentiment_news_data, ticker)
        f_macro = executor.submit(fetch_macro_data, ticker)
        f_risk = executor.submit(fetch_risk_metrics, ticker)
        f_industry = executor.submit(fetch_industry_metrics, ticker)
        f_analyst = executor.submit(fetch_analyst_ratings, ticker)
        
        financial_data = f_financial.result()
        company_profile = f_profile.result()
        roadmap_data = f_roadmap.result()
        sentiment_data = f_sentiment.result()
        macro_data = f_macro.result()
        risk_metrics = f_risk.result()
        industry_metrics = f_industry.result()
        analyst_ratings = f_analyst.result()
        
    return {
        "financial_data": financial_data,
        "company_profile": company_profile,
        "roadmap_data": roadmap_data,
        "sentiment_data": sentiment_data,
        "news_baseline": sentiment_data,
        "macro_data": macro_data,
        "risk_metrics": risk_metrics,
        "industry_metrics": industry_metrics,
        "analyst_ratings": analyst_ratings
    }
