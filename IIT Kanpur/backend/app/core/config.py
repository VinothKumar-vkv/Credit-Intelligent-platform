import os
from typing import List

class Settings:
    def __init__(self):
        # Hardcoded defaults - no environment variable parsing
        self.api_host = "0.0.0.0"
        self.api_port = 8000
        self.log_level = "INFO"
        self.database_url = "sqlite+aiosqlite:///./local.db"
        self.model_dir = "./data/model"
        self.data_dir = "./data"
        self.scheduler_interval_seconds = 300
        self.issuers = "AAPL,MSFT,TSLA,AMZN"
        self.alpha_vantage_key = ""
        self.yf_user_agent = "credit-intel-platform/1.0"
        self.news_rss_feeds = "https://news.google.com/rss/search?q=AAPL,https://news.google.com/rss/search?q=MSFT"

    @property
    def issuers_list(self) -> List[str]:
        return [x.strip() for x in self.issuers.split(",") if x.strip()]

    @property
    def news_rss_feeds_list(self) -> List[str]:
        return [x.strip() for x in self.news_rss_feeds.split(",") if x.strip()]

settings = Settings()
