from __future__ import annotations
import aiohttp
from typing import Optional, Dict

API_BASE = "https://api.worldbank.org/v2"

async def fetch_indicator_latest(country_code: str, indicator: str) -> Optional[float]:
    url = f"{API_BASE}/country/{country_code}/indicator/{indicator}?format=json"
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            if not isinstance(data, list) or len(data) < 2:
                return None
            series = data[1] or []
            for row in series:
                val = row.get("value")
                if val is not None:
                    try:
                        return float(val)
                    except Exception:
                        return None
            return None

async def fetch_macro_features(country_code: str = "USA") -> Dict[str, float]:
    # CPI YoY (%), GDP growth (%); latest available annual values
    cpi = await fetch_indicator_latest(country_code, "FP.CPI.TOTL.ZG")
    gdp = await fetch_indicator_latest(country_code, "NY.GDP.MKTP.KD.ZG")
    return {
        "macro_cpi_yoy": float(cpi) if cpi is not None else 0.0,
        "macro_gdp_growth": float(gdp) if gdp is not None else 0.0,
    }

