# notification_service/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # URL для подключения к RabbitMQ (тот же, что и в order_service)
    rabbitmq_url: str = "amqp://orderflow:orderflow_secret@localhost:5672/"
    queue_name: str = "new_orders"

    # URL нашего order_service для обновления статуса
    order_service_url: str = "http://localhost:8002"


settings = Settings()