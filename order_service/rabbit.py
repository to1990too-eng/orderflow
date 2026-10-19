# order_service/rabbit.py
import json

import aio_pika
from aio_pika import DeliveryMode, Message

from order_service.config import settings

_connection: aio_pika.RobustConnection | None = None
_channel: aio_pika.RobustChannel | None = None

async def init_rabbit() -> None:
    global _connection, _channel
    _connection = await aio_pika.connect_robust(settings.rabbitmq_url)
    _channel = await _connection.channel()
    # Объявляем очередь durable (сообщения выживают при рестарте RabbitMQ)
    await _channel.declare_queue(settings.queue_name, durable=True)
    print(f"[RabbitMQ] Connected, queue '{settings.queue_name}' declared")

async def close_rabbit() -> None:
    global _connection
    if _connection and not _connection.is_closed:
        await _connection.close()
        print("[RabbitMQ] Connection closed")
        _connection = None

async def publish_order_created(order_id: int, user_id: int, item_name: str) -> None:
    if _channel is None:
        raise RuntimeError("RabbitMQ channel not initialized")

    body = json.dumps({
        "order_id": order_id,
        "user_id": user_id,
        "item_name": item_name,
    }).encode()

    message = Message(
        body=body,
        content_type="application/json",
        delivery_mode=DeliveryMode.PERSISTENT,  # Сообщение сохраняется на диск
    )
    await _channel.default_exchange.publish(
        message,
        routing_key=settings.queue_name,
    )
    print(f"[RabbitMQ] Published order {order_id} to '{settings.queue_name}'")