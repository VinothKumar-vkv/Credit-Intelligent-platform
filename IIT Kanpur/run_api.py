#!/usr/bin/env python3
"""
Simple script to run the credit intelligence API
"""
import uvicorn
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set environment variables programmatically
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./local.db'
os.environ['ISSUERS'] = 'AAPL,MSFT,TSLA,AMZN'
os.environ['NEWS_RSS_FEEDS'] = 'https://news.google.com/rss/search?q=AAPL,https://news.google.com/rss/search?q=MSFT'
os.environ['SCHEDULER_INTERVAL_SECONDS'] = '300'

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
