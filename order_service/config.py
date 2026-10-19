# order_service/config.py
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[1] / ".env"

class Settings(BaseSettings):
    # Заменили localhost на postgres
    database_url_orders: str = "postgresql+asyncpg://orderflow:orderflow_secret@postgres:5432/orderflow_orders"

    secret_key: str = "super-secret-key-change-in-production-abc123"
    algorithm: str = "HS256"

    # Заменили localhost на rabbitmq
    rabbitmq_url: str = "amqp://orderflow:orderflow_secret@rabbitmq:5672/"
    queue_name: str = "new_orders"

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()