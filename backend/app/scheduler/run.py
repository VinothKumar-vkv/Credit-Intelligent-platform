import asyncio
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db.session import AsyncSessionLocal
from ..models.models import Issuer, FeatureSnapshot, Score, Event, Alert, ModelMeta
from ..sources.yahoo import fetch_price_history
from ..sources.rss import parse_rss
from ..sources.worldbank import fetch_macro_features
from ..services.features import compute_market_features, compute_risk_target
from ..services.scoring import OnlineModel
import numpy as np

# Hardcoded configuration to avoid pydantic-settings issues
ISSUERS = ["AAPL", "MSFT", "TSLA", "AMZN"]
NEWS_RSS_FEEDS = ["https://news.google.com/rss/search?q=AAPL", "https://news.google.com/rss/search?q=MSFT"]
SCHEDULER_INTERVAL_SECONDS = 300

FEATURE_ORDER = ["vol_7", "vol_30", "drawdown", "mom_7", "mom_30", "liquidity", "macro_cpi_yoy", "macro_gdp_growth"]

async def ensure_seed_issuers(session: AsyncSession) -> None:
    for t in ISSUERS:
        res = await session.execute(select(Issuer).where(Issuer.ticker == t))
        if res.scalar_one_or_none() is None:
            session.add(Issuer(ticker=t, name=t, sector=None))
    await session.commit()

async def ingest_and_score() -> None:
    async with AsyncSessionLocal() as session:
        print("Ensuring seed issuers...")
        await ensure_seed_issuers(session)
        
        # Unstructured news ingestion once per cycle
        print("Processing news feeds...")
        if NEWS_RSS_FEEDS:
            try:
                news = parse_rss(NEWS_RSS_FEEDS)
                print(f"Found {len(news)} news items")
                for n in news[:200]:
                    issuer_id = None
                    tickers = ISSUERS
                    for t in tickers:
                        if t in (n.get("title") or ""):
                            res = await session.execute(select(Issuer).where(Issuer.ticker == t))
                            iss = res.scalar_one_or_none()
                            if iss:
                                issuer_id = iss.id
                                break
                    if issuer_id is None:
                        continue
                    e = Event(issuer_id=issuer_id, source=n["source"], title=n["title"], url=n.get("url"), published_at=n["published_at"], sentiment=n.get("sentiment"))
                    session.add(e)
                await session.commit()
                print(f"Added {len(news[:200])} news events")
            except Exception as e:
                print(f"Error processing news: {e}")

        print("Creating scoring model...")
        model = OnlineModel.create(FEATURE_ORDER)

        print("Fetching macroeconomic data...")
        try:
            macro = await fetch_macro_features("USA")
            print(f"Macro features: {macro}")
        except Exception as e:
            print(f"Error fetching macro data: {e}")
            macro = {"macro_cpi_yoy": 0.0, "macro_gdp_growth": 0.0}

        print("Processing issuers...")
        for t in ISSUERS:
            try:
                print(f"Processing issuer: {t}")
                res = await session.execute(select(Issuer).where(Issuer.ticker == t))
                issuer = res.scalar_one_or_none()
                if issuer is None:
                    print(f"Issuer {t} not found in database")
                    continue
                
                print(f"Fetching price history for {t}...")
                df = await fetch_price_history(t)
                
                if df is None or df.empty:
                    print(f"No data received for {t}, skipping...")
                    continue
                
                print(f"Got {len(df)} data points for {t}")
                feats = compute_market_features(df)
                feats.update(macro)
                target = compute_risk_target(feats)
                
                print(f"Features for {t}: {feats}")
                print(f"Target for {t}: {target}")

                X = np.array([[feats.get(f, 0.0) for f in FEATURE_ORDER]])
                y = np.array([target])
                model.partial_fit(X, y)

                score, contribs = model.predict(feats)
                now = datetime.now(timezone.utc)
                
                print(f"Score for {t}: {score}")
                print(f"Contributions for {t}: {contribs}")

                fs = FeatureSnapshot(issuer_id=issuer.id, as_of=now, features=feats)
                sc = Score(issuer_id=issuer.id, as_of=now, score=float(score), contributions=contribs)
                session.add_all([fs, sc])

                # Check for significant score changes
                prev = await session.execute(select(Score).where(Score.issuer_id == issuer.id).order_by(Score.as_of.desc()).limit(2))
                prev_rows = prev.scalars().all()
                if len(prev_rows) >= 1:
                    prev_score = prev_rows[0].score
                    if abs(score - prev_score) > max(0.1, 0.2 * abs(prev_score)):
                        alert = Alert(issuer_id=issuer.id, kind="score_jump", message=f"Score changed from {prev_score:.2f} to {score:.2f}", payload={"from": prev_score, "to": score})
                        session.add(alert)
                        print(f"Alert created for {t}: score changed from {prev_score:.2f} to {score:.2f}")
                
                print(f"Successfully processed {t}")
                
            except Exception as e:
                print(f"Error processing {t}: {e}")
                continue

        print("Committing all changes...")
        await session.commit()
        print("Data ingestion cycle completed successfully!")

async def main() -> None:
    interval = max(60, SCHEDULER_INTERVAL_SECONDS)
    print(f"Starting Credit Intelligence Scheduler (interval: {interval}s)")
    while True:
        try:
            print(f"\n[{datetime.now()}] Starting data ingestion cycle...")
            await ingest_and_score()
            print(f"[{datetime.now()}] Completed data ingestion cycle")
        except Exception as e:
            print(f"[{datetime.now()}] Error in ingestion cycle: {e}")
            import traceback
            traceback.print_exc()
        print(f"Waiting {interval} seconds until next cycle...")
        await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(main())
