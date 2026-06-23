import yfinance as yf
import pandas as pd
import numpy as np
from tools.retry_utils import with_retry

@with_retry(max_retries=3)
def fetch_technical_indicators(ticker: str) -> str:
    """Fetches technical analysis indicators (RSI, MACD, Bollinger Bands, Support/Resistance) for a ticker."""
    try:
        stock = yf.Ticker(ticker)
        # Fetch 6 months of daily data for technicals
        hist = stock.history(period="6mo")
        if hist.empty:
            return f"Error: No historical data available to calculate technicals for {ticker}."
            
        close = hist["Close"]
        
        # 1. RSI (14-day)
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        # 2. MACD (12-day EMA - 26-day EMA)
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        macd_hist = macd_line - signal_line
        
        current_macd = macd_line.iloc[-1]
        current_signal = signal_line.iloc[-1]
        
        # 3. Bollinger Bands (20-day SMA, 2 standard deviations)
        sma20 = close.rolling(window=20).mean()
        std20 = close.rolling(window=20).std()
        upper_band = sma20 + (std20 * 2)
        lower_band = sma20 - (std20 * 2)
        
        current_price = close.iloc[-1]
        c_upper = upper_band.iloc[-1]
        c_lower = lower_band.iloc[-1]
        
        # 4. Support and Resistance (Basic 3-month lookback min/max)
        recent_3mo = close.tail(63) # approx 63 trading days in 3 months
        support = recent_3mo.min()
        resistance = recent_3mo.max()
        
        # 5. Volume Trend
        avg_volume_10d = hist["Volume"].tail(10).mean()
        current_volume = hist["Volume"].iloc[-1]
        
        report = [
            f"--- Technical Analysis Indicators for {ticker.upper()} ---",
            f"Current Price: ${current_price:.2f}",
            "",
            f"Momentum (RSI-14): {current_rsi:.2f} " + 
                ("(Oversold)" if current_rsi < 30 else "(Overbought)" if current_rsi > 70 else "(Neutral)"),
            f"MACD (12,26,9): Line={current_macd:.2f}, Signal={current_signal:.2f} " +
                ("(Bullish Crossover)" if current_macd > current_signal else "(Bearish Crossover)"),
            "",
            f"Bollinger Bands (20,2):",
            f"  Upper Band: ${c_upper:.2f}",
            f"  Lower Band: ${c_lower:.2f}",
            f"  Band Width: {((c_upper - c_lower) / sma20.iloc[-1] * 100):.1f}%",
            "",
            f"Key Price Levels (3-Month):",
            f"  Support Floor: ${support:.2f} (-{((current_price - support) / current_price * 100):.1f}% from current)",
            f"  Resistance Ceiling: ${resistance:.2f} (+{((resistance - current_price) / current_price * 100):.1f}% from current)",
            "",
            f"Volume Analysis:",
            f"  Today's Volume: {current_volume:,.0f}",
            f"  10-Day Avg Volume: {avg_volume_10d:,.0f}"
        ]
        
        return "\n".join(report)
        
    except Exception as e:
        return f"Error fetching technical data for {ticker}: {str(e)}"
