import yfinance as yf

def fetch_macro_data(ticker: str) -> str:
    """Programmatic backend fetcher for baseline macroeconomic indices comparison."""
    try:
        spy = yf.Ticker("SPY")
        qqq = yf.Ticker("QQQ")
        
        spy_info = spy.info
        qqq_info = qqq.info
        
        spy_price = spy_info.get("currentPrice") or spy_info.get("regularMarketPreviousClose")
        qqq_price = qqq_info.get("currentPrice") or qqq_info.get("regularMarketPreviousClose")
        
        output = [
            f"--- Macro Benchmark Metrics ---",
            f"- SPY (S&P 500 ETF) Price: ${spy_price:.2f}" if spy_price else "- SPY Price: N/A",
            f"- QQQ (Nasdaq 100 ETF) Price: ${qqq_price:.2f}" if qqq_price else "- QQQ Price: N/A",
            f"- Analysis Baseline: Evaluating against broader market benchmark indices."
        ]
        return "\n".join(output)
    except Exception as e:
        return f"Error fetching macro benchmarking data: {e}"


def fetch_industry_metrics(ticker: str) -> str:
    """Fetches industry-level or sector-level comparative metrics for the target ticker using yfinance."""
    try:
        t = yf.Ticker(ticker)
        info = t.info
        
        industry = info.get("industry", "N/A")
        sector = info.get("sector", "N/A")
        
        # Pull peer or industry comparative indicators if available
        peg = info.get("pegRatio", "N/A")
        profit_margins = info.get("profitMargins")
        margins_str = f"{profit_margins * 100:.2f}%" if profit_margins is not None else "N/A"
        debt_to_equity = info.get("debtToEquity")
        d2e_str = f"{debt_to_equity:.2f}" if debt_to_equity is not None else "N/A"
        price_to_book = info.get("priceToBook")
        p2b_str = f"{price_to_book:.2f}" if price_to_book is not None else "N/A"
        
        output = [
            f"--- Sector & Industry Fundamentals for {ticker.upper()} ---",
            f"- Sector: {sector}",
            f"- Industry: {industry}",
            f"- PEG Ratio: {peg}",
            f"- Profit Margins: {margins_str}",
            f"- Debt-to-Equity: {d2e_str}",
            f"- Price-to-Book: {p2b_str}",
            f"- Note: Sector valuations and peer indicators derived from live fundamental data."
        ]
        return "\n".join(output)
    except Exception as e:
        return f"Error fetching industry comparison metrics: {e}"
