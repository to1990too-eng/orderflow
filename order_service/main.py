# order_service/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from order_service.api.orders import router as orders_router
from order_service.database import engine
from order_service.models import Base
from order_service.rabbit import close_rabbit, init_rabbit


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_rabbit()  # Инициализация RabbitMQ (Шаг 4)
    yield
    await close_rabbit()
    await engine.dispose()

app = FastAPI(title="OrderFlow Order Service", lifespan=lifespan)
app.include_router(orders_router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "order_service"}