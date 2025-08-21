from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...db.session import get_session
from ...models.models import Event
from ...schemas.schemas import EventOut

router = APIRouter()

@router.get("/", response_model=list[EventOut])
async def list_events(limit: int = 100, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Event).order_by(Event.published_at.desc()).limit(limit))
    return res.scalars().all()

