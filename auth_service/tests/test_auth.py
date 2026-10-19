# auth_service/tests/test_auth.py
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from auth_service.database import get_db
from auth_service.main import app
from auth_service.models import Base

# Используем SQLite в памяти для тестов
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
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


@pytest_asyncio.fixture
async def client(test_db):
    # В новых версиях httpx используется ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_register_and_login(client):
    # 1. Регистрация
    response = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "strongpassword"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

    # 2. Логин
    response = await client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "strongpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()