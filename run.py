from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
from config import TOKEN
import asyncio

from app.database import create
from app.handlers import router
from app.scheduler import send_reminders

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()


async def on_startup():
    """Запуск планировщика при старте бота"""
    scheduler.add_job(send_reminders, "interval", minutes=1, args=[bot])
    scheduler.start()


async def main():
    dp.include_router(router)
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(create())
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
