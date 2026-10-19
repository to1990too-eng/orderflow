# auth_service/database.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from auth_service.config import settings

# Создаём асинхронный движок
engine = create_async_engine(
    settings.database_url_auth,
    echo=True,          # Логирование SQL — удобно на старте, потом выключи
    pool_pre_ping=True, # Проверка соединения перед использованием
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Важно для async: объекты остаются доступны после commit
)

# Зависимость для FastAPI (инжектится в роутеры)
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()