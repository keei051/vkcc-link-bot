import logging
import os
import json
import aiohttp
import asyncio
import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import escape_md
from asyncio import Semaphore
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
VK_TOKEN = os.getenv("VK_TOKEN")

if not BOT_TOKEN or not VK_TOKEN:
    logging.error("BOT_TOKEN or VK_TOKEN not found in .env file")
    exit(1)

# Настройки
MAX_BULK_LINKS = 50
HEADERS = {"Authorization": f"Bearer {VK_TOKEN}"}

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# Валидация URL
url_pattern = re.compile(r"https?://[^\s]+")

# Отправка длинных сообщений
async def send_long_message(message: Message, text: str, max_length=4096):
    if len(text) <= max_length:
        await message.answer(text, disable_web_page_preview=True)
        return
    parts = [text[i:i + max_length] for i in range(0, len(text), max_length)]
    for part in parts:
        await message.answer(part, disable_web_page_preview=True)

# Сокращение одной ссылки
async def shorten_url(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get("https://vk.cc/shorten", params={"url": url}, headers=HEADERS) as r:
                if r.status == 200:
                    data = await r.json()
                    short_url = data.get("short_url")
                    if short_url:
                        return f"✅ [{escape_md(url)}]({escape_md(short_url)})"
                    else:
                        return f"⚠️ `{escape_md(url)}` — ошибка при сокращении"
                return f"⚠️ `{escape_md(url)}` — не удалось сократить (статус: {r.status})"
        except aiohttp.ClientError as e:
            return f"⚠️ `{escape_md(url)}` — ошибка сети: {str(e)}"

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("🔗 Привет! Отправь ссылку или сразу несколько (до 50), и я их сокращу.\n\nЧтобы начать заново, набери /start")

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Отправь ссылку или сразу несколько (каждая с новой строки).\n\nЯ сокращу и верну статистику!")

@dp.message(F.text)
async def handle_links(message: Message):
    raw_text = message.text.strip()
    lines = list(filter(None, raw_text.splitlines()))
    if not lines:
        await message.answer("⚠️ Не вижу ссылок. Попробуй ещё раз.")
        return

    if len(lines) > MAX_BULK_LINKS:
        await message.answer(f"⚠️ Можно отправить не больше {MAX_BULK_LINKS} ссылок за раз.")
        return

    semaphore = Semaphore(5)
    async with aiohttp.ClientSession() as session:
        tasks = [shorten_url(session, line, semaphore) for line in lines if url_pattern.match(line)]
        result = await asyncio.gather(*tasks)
        result.extend([f"❌ `{escape_md(line)}` — не ссылка" for line in lines if not url_pattern.match(line)])

    success_count = sum(1 for r in result if r.startswith("✅"))
    await send_long_message(message, f"📊 Сокращено: {success_count}/{len(lines)}\n\n" + "\n\n".join(result))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
