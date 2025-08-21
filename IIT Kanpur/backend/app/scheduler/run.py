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

FEATURE_ORDER = ["vol_7", "vol_30", "drawdown", "mom_7", "mom_30", "liquidity", "macro_cpi_yoy", "macro_gdp_growth"]

# Hardcoded settings
ISSUERS = ["AAPL", "MSFT", "TSLA", "AMZN"]
NEWS_RSS_FEEDS = ["https://news.google.com/rss/search?q=AAPL", "https://news.google.com/rss/search?q=MSFT"]
SCHEDULER_INTERVAL_SECONDS = 300

async def ensure_seed_issuers(session: AsyncSession) -> None:
    for t in ISSUERS:
        res = await session.execute(select(Issuer).where(Issuer.ticker == t))
        if res.scalar_one_or_none() is None:
            session.add(Issuer(ticker=t, name=t, sector=None))
    await session.commit()

async def ingest_and_score() -> None:
    async with AsyncSessionLocal() as session:
        await ensure_seed_issuers(session)
        # Unstructured news ingestion once per cycle
        if NEWS_RSS_FEEDS:
            news = parse_rss(NEWS_RSS_FEEDS)
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

        model = OnlineModel.create(FEATURE_ORDER)

        macro = await fetch_macro_features("USA")

        for t in ISSUERS:
            res = await session.execute(select(Issuer).where(Issuer.ticker == t))
            issuer = res.scalar_one_or_none()
            if issuer is None:
                continue
            df = await fetch_price_history(t)
            if df is None or df.empty:
                continue
            feats = compute_market_features(df)
            feats.update(macro)
            target = compute_risk_target(feats)

            X = np.array([[feats.get(f, 0.0) for f in FEATURE_ORDER]])
            y = np.array([target])
            model.partial_fit(X, y)

            score, contribs = model.predict(feats)
            now = datetime.now(timezone.utc)

            fs = FeatureSnapshot(issuer_id=issuer.id, as_of=now, features=feats)
            sc = Score(issuer_id=issuer.id, as_of=now, score=float(score), contributions=contribs)
            session.add_all([fs, sc])

            prev = await session.execute(select(Score).where(Score.issuer_id == issuer.id).order_by(Score.as_of.desc()).limit(2))
            prev_rows = prev.scalars().all()
            if len(prev_rows) >= 1:
                prev_score = prev_rows[0].score
                if abs(score - prev_score) > max(0.1, 0.2 * abs(prev_score)):
                    session.add(Alert(issuer_id=issuer.id, kind="score_jump", message=f"Score changed from {prev_score:.2f} to {score:.2f}", payload={"from": prev_score, "to": score}))

        await session.commit()

async def main() -> None:
    interval = max(60, SCHEDULER_INTERVAL_SECONDS)
    while True:
        try:
            await ingest_and_score()
        except Exception:
            pass
        await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(main())
