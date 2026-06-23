import yfinance as yf

def fetch_risk_metrics(ticker: str) -> str:
    """Programmatic backend fetcher for downside volatility, beta, and short interest statistics."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        risk = {
            "Beta (5Y Monthly)": info.get("beta"),
            "Short % of Float": info.get("shortPercentOfFloat"),
            "Shares Short": info.get("sharesShort"),
            "Shares Short Prior Month": info.get("sharesShortPriorMonth"),
            "Implied Options Volatility (Proxy)": info.get("impliedVolatility"),
        }
        
        output = [f"--- Volatility & Risk Metrics for {ticker.upper()} ---"]
        for k, v in risk.items():
            if v is None:
                output.append(f"- {k}: N/A")
            elif k == "Short % of Float" and isinstance(v, (int, float)):
                output.append(f"- {k}: {v * 100:.2f}%")
            elif k in ["Shares Short", "Shares Short Prior Month"] and isinstance(v, (int, float)):
                output.append(f"- {k}: {v:,}")
            elif isinstance(v, (int, float)):
                output.append(f"- {k}: {v:.2f}")
            else:
                output.append(f"- {k}: {v}")
        return "\n".join(output)
    except Exception as e:
        return f"Error fetching risk indicators: {e}"
