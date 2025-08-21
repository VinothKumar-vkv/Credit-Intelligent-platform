from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...db.session import get_session
from ...models.models import Alert
from ...schemas.schemas import AlertOut

router = APIRouter()

@router.get("/", response_model=list[AlertOut])
async def list_alerts(limit: int = 100, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Alert).order_by(Alert.created_at.desc()).limit(limit))
    return res.scalars().all()

