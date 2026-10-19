# order_service/tests/test_orders.py
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from order_service.database import get_db
from order_service.main import app
from order_service.models import Base
from order_service.security import get_current_user_id

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def test_db():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    TestSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session
            await session.commit()

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    await engine.dispose()


@pytest.fixture
async def client(test_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_current_user():
    # Подменяем проверку JWT, чтобы не генерировать токен в тестах
    app.dependency_overrides[get_current_user_id] = lambda: 1
    yield
    app.dependency_overrides.pop(get_current_user_id, None)


@pytest.mark.asyncio
@patch("order_service.api.orders.publish_order_created", new_callable=AsyncMock)
async def test_create_order(mock_publish, client, mock_current_user):
    response = await client.post("/api/v1/orders", json={
        "item_name": "Тестовый ноутбук",
        "price": 1000
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"

    # Проверяем, что "сообщение в RabbitMQ" было отправлено
    mock_publish.assert_called_once()