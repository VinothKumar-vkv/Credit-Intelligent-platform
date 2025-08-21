from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List

class IssuerCreate(BaseModel):
    ticker: str
    name: str
    sector: Optional[str] = None

class IssuerOut(BaseModel):
    id: int
    ticker: str
    name: str
    sector: Optional[str]

    class Config:
        from_attributes = True

class EventOut(BaseModel):
    id: int
    issuer_id: int
    source: str
    title: str
    url: Optional[str]
    published_at: datetime
    sentiment: Optional[float]
    meta: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True

class FeatureSnapshotOut(BaseModel):
    id: int
    issuer_id: int
    as_of: datetime
    features: Dict[str, Any]

    class Config:
        from_attributes = True

class ScoreOut(BaseModel):
    id: int
    issuer_id: int
    as_of: datetime
    score: float
    contributions: Optional[Dict[str, float]]
    meta: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True

class AlertOut(BaseModel):
    id: int
    issuer_id: int
    created_at: datetime
    kind: str
    message: str
    payload: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True

class TrendOut(BaseModel):
    issuer_id: int
    timestamps: List[datetime]
    scores: List[float]

