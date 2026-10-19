# notification_service/worker.py
import json
import asyncio
import aio_pika
import httpx
from notification_service.config import settings


async def process_message(message: aio_pika.IncomingMessage):
    # ВАЖНО: Используем async with, чтобы RabbitMQ знал, что мы обрабатываем сообщение
    async with message.process():
        try:
            # 1. Парсим JSON из тела сообщения
            body = json.loads(message.body.decode())
            order_id = body["order_id"]
            item_name = body["item_name"]

            print(f"[Worker] Получено сообщение для заказа {order_id} ({item_name})")

            # 2. Имитируем отправку email (в реальности тут был бы SMTP-клиент)
            print(f"[Worker] 📧 Email sent for order {order_id}")

            # Небольшая задержка, чтобы имитировать работу отправки
            await asyncio.sleep(1)

            # 3. Обновляем статус заказа через HTTP-запрос к order_service
            async with httpx.AsyncClient() as client:
                url = f"{settings.order_service_url}/api/v1/orders/{order_id}/status"
                response = await client.patch(
                    url,
                    json={"status": "processed"},
                    timeout=5.0
                )

                if response.status_code == 200:
                    print(f"[Worker] ✅ Статус заказа {order_id} обновлен на 'processed'")
                else:
                    print(f"[Worker] ❌ Ошибка обновления статуса: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"[Worker] ❌ Ошибка при обработке сообщения: {e}")
            # Если произошла ошибка, message.process() автоматически вернет сообщение в очередь (nack)


async def start_worker():
    """Функция запуска слушателя RabbitMQ"""
    print("[Worker] Запуск notification_service воркера...")

    # Подключаемся к RabbitMQ
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)

    # Создаем канал
    channel = await connection.channel()

    # Говорим RabbitMQ не отправлять больше 1 сообщения за раз (справедливая очередь)
    await channel.set_qos(prefetch_count=1)

    # Объявляем очередь
    queue = await channel.declare_queue(settings.queue_name, durable=True)

    print(f"[Worker] Слушаем очередь '{settings.queue_name}'...")

    # Запускаем бесконечный цикл потребления сообщений
    await queue.consume(process_message)

    # Держим соединение открытым
    return connection