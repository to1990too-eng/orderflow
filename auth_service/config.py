# auth_service/config.py
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Явный путь к .env в корне проекта
ENV_FILE = Path(__file__).resolve().parents[1] / ".env"

class Settings(BaseSettings):
    # База данных
    database_url_auth: str = "postgresql+asyncpg://orderflow:orderflow_secret@localhost:5432/orderflow_auth"

    # JWT
    # secret_key: str  # Берется из .env
    secret_key: str = "super-secret-key-change-in-production-abc123"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()