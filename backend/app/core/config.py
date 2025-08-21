from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os

class Settings(BaseSettings):
    api_host: str = Field(default_factory=lambda: os.getenv("API_HOST", "0.0.0.0"))
    api_port: int = Field(default_factory=lambda: int(os.getenv("API_PORT", "8000")))
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    database_url: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./local.db"))

    model_dir: str = Field(default_factory=lambda: os.getenv("MODEL_DIR", "./data/model"))
    data_dir: str = Field(default_factory=lambda: os.getenv("DATA_DIR", "./data"))

    scheduler_interval_seconds: int = Field(default_factory=lambda: int(os.getenv("SCHEDULER_INTERVAL_SECONDS", "600")))
    issuers: List[str] = Field(default_factory=lambda: [x.strip() for x in os.getenv("ISSUERS", "AAPL,MSFT").split(",") if x.strip()])

    alpha_vantage_key: str = Field(default_factory=lambda: os.getenv("ALPHA_VANTAGE_KEY", ""))
    yf_user_agent: str = Field(default_factory=lambda: os.getenv("YF_USER_AGENT", "credit-intel-platform/1.0"))

    news_rss_feeds: List[str] = Field(default_factory=lambda: [x.strip() for x in os.getenv("NEWS_RSS_FEEDS", "").split(",") if x.strip()])

settings = Settings()

