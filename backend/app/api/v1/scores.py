from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...db.session import get_session
from ...models.models import Score
from ...schemas.schemas import ScoreOut, TrendOut

router = APIRouter()

@router.get("/", response_model=list[ScoreOut])
async def list_scores(issuer_id: int | None = None, limit: int = 100, session: AsyncSession = Depends(get_session)):
    stmt = select(Score).order_by(Score.as_of.desc()).limit(limit)
    if issuer_id:
        stmt = stmt.where(Score.issuer_id == issuer_id)
    res = await session.execute(stmt)
    return res.scalars().all()

@router.get("/trend", response_model=TrendOut)
async def score_trend(issuer_id: int, limit: int = 200, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Score).where(Score.issuer_id == issuer_id).order_by(Score.as_of.asc()).limit(limit))
    rows = res.scalars().all()
    return {
        "issuer_id": issuer_id,
        "timestamps": [r.as_of for r in rows],
        "scores": [r.score for r in rows],
    }

