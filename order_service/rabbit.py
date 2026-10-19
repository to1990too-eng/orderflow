# order_service/rabbit.py

async def publish_order_created(order_id: int, user_id: int, item_name: str) -> None:
    print(f"[RABBITMQ STUB] Would publish order {order_id} for user {user_id}")

async def init_rabbit():
    print("[RABBITMQ STUB] Инициализация RabbitMQ")
    return None

async def close_rabbit():
    print("[RABBITMQ STUB] Закрытие соединения RabbitMQ")
    return None