# auth_service/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from auth_service.database import engine
from auth_service.models import Base
from auth_service.api.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # На старте создаём таблицы (для продакшена лучше Alembic, но для портфолио ок)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="OrderFlow Auth Service", lifespan=lifespan)

app.include_router(auth_router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "auth_service"}