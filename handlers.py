import re
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from utils import is_valid_url, shorten_vk_link, send_long_message

router = Router()

MAX_BULK_LINKS = 50

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("🔗 Привет! Отправь ссылку или сразу несколько (до 50), и я их сокращу.\n\nЧтобы начать заново, набери /start")

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Отправь ссылку или сразу несколько (каждая с новой строки).\n\nЯ сокращу и верну статистику!")

@router.message(F.text)
async def handle_links(message: Message):
    raw_text = message.text.strip()
    lines = list(filter(None, raw_text.splitlines()))

    if not lines:
        await message.answer("⚠️ Не вижу ссылок. Попробуй ещё раз.")
        return

    if len(lines) > MAX_BULK_LINKS:
        await message.answer(f"⚠️ Можно отправить не больше {MAX_BULK_LINKS} ссылок за раз.")
        return

    result = []
    success = 0

    for line in lines:
        if not is_valid_url(line):
            result.append(f"❌ `{line}` — не ссылка")
            continue

        short = await shorten_vk_link(line)
        if short:
            success += 1
            result.append(f"✅ [{line}]({short})")
        else:
            result.append(f"⚠️ `{line}` — ошибка при сокращении")

    summary = f"📊 Сокращено: {success}/{len(lines)}\n\n"
    await send_long_message(message, summary + "\n\n".join(result))
