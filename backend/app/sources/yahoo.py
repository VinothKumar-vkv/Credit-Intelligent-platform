from __future__ import annotations
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
import asyncio

async def fetch_price_history(ticker: str, days: int = 120) -> pd.DataFrame:
    """Fetch price history with fallback to generated data if Yahoo Finance fails"""
    try:
        end = datetime.now(timezone.utc)
        start = end - timedelta(days=days)
        
        # Try to fetch from Yahoo Finance
        df = yf.download(ticker, start=start.date(), end=end.date(), progress=False, auto_adjust=True, threads=False)
        
        if df is not None and not df.empty:
            df = df.rename(columns={"Close": "close", "Volume": "volume"})
            return df[["close", "volume"]].reset_index(drop=False).rename(columns={"Date": "date"})
        
    except Exception as e:
        print(f"Yahoo Finance failed for {ticker}: {e}")
    
    # Fallback: Generate synthetic data for demo purposes
    print(f"Using fallback data for {ticker}")
    return generate_fallback_data(ticker, days)

def generate_fallback_data(ticker: str, days: int) -> pd.DataFrame:
    """Generate realistic fallback data for demo purposes"""
    end = datetime.now(timezone.utc)
    dates = [end - timedelta(days=i) for i in range(days, 0, -1)]
    
    # Base prices for different tickers
    base_prices = {
        "AAPL": 150.0,
        "MSFT": 300.0,
        "TSLA": 200.0,
        "AMZN": 120.0
    }
    
    base_price = base_prices.get(ticker, 100.0)
    
    # Generate realistic price movements
    np.random.seed(hash(ticker) % 1000)  # Consistent but different for each ticker
    returns = np.random.normal(0.001, 0.02, days)  # Daily returns with volatility
    prices = [base_price]
    
    for ret in returns[1:]:
        new_price = prices[-1] * (1 + ret)
        prices.append(max(new_price, 1.0))  # Ensure price doesn't go below $1
    
    # Generate volume data
    volumes = np.random.lognormal(15, 0.5, days).astype(int)
    
    df = pd.DataFrame({
        "date": dates,
        "close": prices,
        "volume": volumes
    })
    
    return df

