# notification_service/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # URL для подключения к RabbitMQ (имя сервиса rabbitmq)
    rabbitmq_url: str = "amqp://orderflow:orderflow_secret@rabbitmq:5672/"
    queue_name: str = "new_orders"

    # URL нашего order_service (имя сервиса order_service)
    order_service_url: str = "http://order_service:8002"


settings = Settings()