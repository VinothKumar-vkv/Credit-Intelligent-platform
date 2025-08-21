from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...db.session import get_session
from ...models.models import Issuer
from ...schemas.schemas import IssuerCreate, IssuerOut

router = APIRouter()

@router.get("/", response_model=list[IssuerOut])
async def list_issuers(session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Issuer))
    return res.scalars().all()

@router.post("/", response_model=IssuerOut)
async def create_issuer(payload: IssuerCreate, session: AsyncSession = Depends(get_session)):
    exists = await session.execute(select(Issuer).where(Issuer.ticker == payload.ticker))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Ticker already exists")
    issuer = Issuer(ticker=payload.ticker.upper(), name=payload.name, sector=payload.sector)
    session.add(issuer)
    await session.commit()
    await session.refresh(issuer)
    return issuer

