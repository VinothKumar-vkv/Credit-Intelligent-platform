from __future__ import annotations
import feedparser
from datetime import datetime, timezone
from typing import List, Dict
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def parse_rss(feeds: List[str]) -> List[Dict]:
    items: List[Dict] = []
    for url in feeds:
        try:
            parsed = feedparser.parse(url)
            for e in parsed.entries:
                title = e.get("title", "")
                link = e.get("link", None)
                published = e.get("published_parsed")
                dt = datetime.fromtimestamp(0, tz=timezone.utc)
                if published:
                    dt = datetime(*published[:6], tzinfo=timezone.utc)
                sentiment = float(sia.polarity_scores(title)["compound"]) if title else 0.0
                items.append({
                    "source": "rss",
                    "title": title,
                    "url": link,
                    "published_at": dt,
                    "sentiment": sentiment,
                })
        except Exception:
            continue
    return items

