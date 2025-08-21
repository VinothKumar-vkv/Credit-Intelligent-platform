from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.session import init_db
from .api.routes import api_router

app = FastAPI(title="Credit Intelligence Platform", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup() -> None:
    await init_db()

app.include_router(api_router)
