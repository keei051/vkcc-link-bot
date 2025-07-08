import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv

from database import Database
from keyboards import main_menu
from config import MAX_LINKS_PER_BATCH, BOT_TOKEN, VK_TOKEN
from utils import shorten_vk_link, send_long_message, is_valid_url, escape_md

# Настройка логирования
logging.basicConfig(level=logging.INFO)
load_dotenv()

if not BOT_TOKEN or not VK_TOKEN:
    logging.error("BOT_TOKEN or VK_TOKEN not found in .env")
    exit(1)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()
db = Database()

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "👋 Привет! Отправь одну или сразу несколько ссылок (до 50). Я сокращу их и сохраню.",
        reply_markup=main_menu
    )

@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "📌 Отправь до 50 ссылок (каждая с новой строки), и я верну сокращения."
    )

@dp.message(F.text)
async def handle_text(message: Message):
    user_id = message.from_user.id
    raw = message.text.strip()
    lines = list(filter(None, raw.splitlines()))

    if not lines:
        await message.answer("⚠️ Не вижу ссылок. Попробуй ещё раз.")
        return

    if len(lines) > MAX_LINKS_PER_BATCH:
        await message.answer(f"⚠️ Максимум {MAX_LINKS_PER_BATCH} ссылок за раз.")
        return

    results = []
    success = []

    for line in lines:
        if is_valid_url(line):
            short = await shorten_vk_link(line)
            if short:
                db.add_link(user_id, line, short)
                results.append(f"✅ [{escape_md(line)}]({escape_md(short)})")
                success.append((line, short))
            else:
                results.append(f"⚠️ `{escape_md(line)}` — ошибка при сокращении")
        else:
            results.append(f"❌ `{escape_md(line)}` — невалидная ссылка")

    summary = f"📊 Сокращено: {len(success)}/{len(lines)}\n\n"
    await send_long_message(message, summary + "\n".join(results))

@dp.message(F.text == "Статистика")
async def stats_cmd(message: Message):
    user_id = message.from_user.id
    links = db.get_links(user_id)
    if not links:
        await message.answer("🔍 У тебя пока нет ссылок.")
        return

    text = "📎 Твои ссылки:\n\n"
    for link_id, original, short, title in links:
        name = f"*{escape_md(title)}*" if title else escape_md(original)
        text += f"{name} — [{escape_md(short)}]({escape_md(short)})\n"
    await send_long_message(message, text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
