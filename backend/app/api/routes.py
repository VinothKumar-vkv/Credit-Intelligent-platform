from fastapi import APIRouter
from .v1 import issuers, scores, events, features, alerts, health

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(issuers.router, prefix="/v1/issuers", tags=["issuers"])
api_router.include_router(scores.router, prefix="/v1/scores", tags=["scores"])
api_router.include_router(features.router, prefix="/v1/features", tags=["features"])
api_router.include_router(events.router, prefix="/v1/events", tags=["events"])
api_router.include_router(alerts.router, prefix="/v1/alerts", tags=["alerts"])

