# notification_service/main.py
import asyncio

from notification_service.worker import start_worker


async def main():
    # Запускаем воркер и держим процесс активным
    connection = await start_worker()
    try:
        # Ждем бесконечно, пока процесс не будет убит (Ctrl+C)
        await asyncio.Future()
    finally:
        await connection.close()

if __name__ == "__main__":
    asyncio.run(main())