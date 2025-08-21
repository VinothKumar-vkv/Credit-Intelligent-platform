from __future__ import annotations
import pandas as pd
import numpy as np

# Basic market features from price series

def compute_market_features(df: pd.DataFrame) -> dict:
    # expects columns: close
    series = df["close"].astype(float)
    returns = series.pct_change().dropna()
    vol_7 = returns.rolling(7).std().iloc[-1] if len(returns) >= 7 else returns.std()
    vol_30 = returns.rolling(30).std().iloc[-1] if len(returns) >= 30 else returns.std()
    drawdown = (series / series.cummax() - 1.0).iloc[-1]
    momentum_7 = (series.iloc[-1] / series.iloc[-7] - 1.0) if len(series) >= 7 else 0.0
    momentum_30 = (series.iloc[-1] / series.iloc[-30] - 1.0) if len(series) >= 30 else 0.0
    liquidity_proxy = df.get("volume", pd.Series(index=df.index, data=np.nan)).astype(float).rolling(5).mean().iloc[-1]

    return {
        "vol_7": float(vol_7 if pd.notna(vol_7) else 0.0),
        "vol_30": float(vol_30 if pd.notna(vol_30) else 0.0),
        "drawdown": float(drawdown if pd.notna(drawdown) else 0.0),
        "mom_7": float(momentum_7 if pd.notna(momentum_7) else 0.0),
        "mom_30": float(momentum_30 if pd.notna(momentum_30) else 0.0),
        "liquidity": float(liquidity_proxy if pd.notna(liquidity_proxy) else 0.0),
    }

# Simple target proxy combining volatility, drawdown, and negative momentum into higher risk

def compute_risk_target(features: dict) -> float:
    risk = 0.0
    risk += abs(features.get("vol_7", 0.0)) * 0.4
    risk += abs(features.get("vol_30", 0.0)) * 0.3
    risk += abs(min(features.get("drawdown", 0.0), 0.0)) * 0.2
    risk += abs(min(-features.get("mom_7", 0.0), 0.0)) * 0.1
    return float(risk)

