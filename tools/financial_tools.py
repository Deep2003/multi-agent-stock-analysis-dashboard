import yfinance as yf

def fetch_financial_data(ticker: str) -> str:
    """Programmatic backend fetcher for quantitative financial health metrics."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="250d")
        
        if hist.empty:
            current_price = info.get("currentPrice") or info.get("regularMarketPreviousClose")
            sma_50 = info.get("fiftyDayAverage")
            sma_200 = info.get("twoHundredDayAverage")
            volume = info.get("volume")
        else:
            current_price = float(hist["Close"].iloc[-1])
            sma_50 = float(hist["Close"].tail(50).mean()) if len(hist) >= 50 else None
            sma_200 = float(hist["Close"].tail(200).mean()) if len(hist) >= 200 else None
            volume = int(hist["Volume"].iloc[-1])

        metrics = {
            "Current Price": f"${current_price:.2f}" if current_price else "N/A",
            "50-Day SMA": f"${sma_50:.2f}" if sma_50 else "N/A",
            "200-Day SMA": f"${sma_200:.2f}" if sma_200 else "N/A",
            "Volume": f"{volume:,}" if volume else "N/A",
            "Trailing P/E": info.get("trailingPE"),
            "Forward P/E": info.get("forwardPE"),
            "Market Cap": info.get("marketCap"),
            "EPS (Trailing)": info.get("trailingEps"),
            "Revenue Growth": info.get("revenueGrowth"),
            "Profit Margin": info.get("profitMargins"),
            "Debt-to-Equity": info.get("debtToEquity"),
            "Current Ratio": info.get("currentRatio"),
        }
        
        output = [f"--- Quantitative Financial Data for {ticker.upper()} ---"]
        for k, v in metrics.items():
            if v is None:
                output.append(f"- {k}: N/A")
            elif k == "Market Cap" and isinstance(v, (int, float)):
                output.append(f"- {k}: ${v:,}")
            elif k in ["Revenue Growth", "Profit Margin"] and isinstance(v, (int, float)):
                output.append(f"- {k}: {v * 100:.2f}%")
            elif k in ["Trailing P/E", "Forward P/E", "EPS (Trailing)", "Debt-to-Equity", "Current Ratio"] and isinstance(v, (int, float)):
                output.append(f"- {k}: {v:.2f}")
            else:
                output.append(f"- {k}: {v}")
        return "\n".join(output)
    except Exception as e:
        return f"Error fetching quantitative financials: {e}"


def fetch_company_profile(ticker: str) -> str:
    """Programmatic backend fetcher for company overview and core business sector details."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        profile = {
            "Company Name": info.get("longName"),
            "Sector": info.get("sector"),
            "Industry": info.get("industry"),
            "Business Summary": info.get("longBusinessSummary"),
        }
        
        output = [f"--- Company Profile & Product Overview for {ticker.upper()} ---"]
        for k, v in profile.items():
            if not v:
                output.append(f"- {k}: N/A")
            elif k == "Business Summary":
                output.append(f"\nBusiness Summary:\n{v}")
            else:
                output.append(f"- {k}: {v}")
        return "\n".join(output)
    except Exception as e:
        return f"Error fetching company profile: {e}"


def fetch_analyst_ratings(ticker: str) -> str:
    """Fetches the latest Wall Street analyst consensus and target prices using yfinance."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        target_mean = info.get("targetMeanPrice")
        target_high = info.get("targetHighPrice")
        target_low = info.get("targetLowPrice")
        rec_mean = info.get("recommendationMean") # Typically 1 (Strong Buy) to 5 (Sell)
        rec_key = info.get("recommendationKey", "N/A") # e.g. buy, hold, sell
        
        output = [
            f"--- Wall Street Analyst Consensus for {ticker.upper()} ---",
            f"- Recommendation Key: {rec_key}",
            f"- Recommendation Mean Value: {f'{rec_mean:.2f}' if rec_mean is not None else 'N/A'} (Scale: 1.0 Strong Buy to 5.0 Strong Sell)",
            f"- Mean Price Target: {f'${target_mean:.2f}' if target_mean is not None else 'N/A'}",
            f"- High Price Target: {f'${target_high:.2f}' if target_high is not None else 'N/A'}",
            f"- Low Price Target: {f'${target_low:.2f}' if target_low is not None else 'N/A'}",
            f"- Note: Target prices and consensus gathered from institutional analyst coverage."
        ]
        return "\n".join(output)
    except Exception as e:
        return f"Error fetching analyst ratings: {e}"
