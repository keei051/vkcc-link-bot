from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from utils import shorten_vk_link, send_long_message, is_valid_url, escape_md

router = Router()

MAX_LINKS = 50

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Отправь одну или сразу несколько ссылок (по одной на строку) — я сокращу их через vk.cc"
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📌 Просто отправь ссылки (до 50 штук за раз).\n"
        "Я сокращу их и верну результат."
    )

@router.message(F.text)
async def handle_links(message: Message):
    raw = message.text.strip()
    lines = list(filter(None, raw.splitlines()))

    if not lines:
        await message.answer("⚠️ Не вижу ссылок. Попробуй ещё раз.")
        return

    if len(lines) > MAX_LINKS:
        await message.answer(f"⚠️ Можно сократить не больше {MAX_LINKS} ссылок за раз.")
        return

    result = []
    success_count = 0

    for line in lines:
        if is_valid_url(line):
            short = await shorten_vk_link(line)
            if short:
                result.append(f"✅ [{escape_md(line)}]({escape_md(short)})")
                success_count += 1
            else:
                result.append(f"⚠️ `{escape_md(line)}` — ошибка при сокращении")
        else:
            result.append(f"❌ `{escape_md(line)}` — невалидная ссылка")

    summary = f"📊 Сокращено: {success_count}/{len(lines)}\n\n"
    await send_long_message(message, summary + "\n".join(result))
