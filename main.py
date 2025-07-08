import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from dotenv import load_dotenv
from handlers import router as handlers_router

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing in .env")

# Инициализация
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
dp = Dispatcher()
dp.include_router(handlers_router)
logging.basicConfig(level=logging.INFO)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
