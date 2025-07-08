import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import setup_handlers
from database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    await init_db()
    setup_handlers(dp)

    webhook_info = await bot.get_webhook_info()
    if webhook_info.url:
        await bot.delete_webhook()
        logger.info("Webhook удалён")

    logger.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
