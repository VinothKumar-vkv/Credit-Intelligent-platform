from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...db.session import get_session
from ...models.models import FeatureSnapshot
from ...schemas.schemas import FeatureSnapshotOut

router = APIRouter()

@router.get("/", response_model=list[FeatureSnapshotOut])
async def list_features(issuer_id: int | None = None, limit: int = 100, session: AsyncSession = Depends(get_session)):
    stmt = select(FeatureSnapshot).order_by(FeatureSnapshot.as_of.desc()).limit(limit)
    if issuer_id:
        stmt = stmt.where(FeatureSnapshot.issuer_id == issuer_id)
    res = await session.execute(stmt)
    return res.scalars().all()

