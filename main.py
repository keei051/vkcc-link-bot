import os
import re
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from utils import shorten_vk_link, send_long_message

# Загрузка токенов из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверка токена
if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN не найден в .env")
    exit(1)

# Настройки
MAX_BULK_LINKS = 50
url_pattern = re.compile(r"https?://[^\s]+")

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
dp = Dispatcher()

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сократить ссылку")],
        [KeyboardButton(text="Статистика")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие"
)

# Команда /start
@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я умею сокращать ссылки через VK.cc\n\n"
        "Отправь одну или сразу несколько ссылок (каждая с новой строки).\n"
        "Максимум — 50 за раз.",
        reply_markup=main_menu
    )

# Команда /help
@dp.message(F.text == "/help")
async def cmd_help(message: Message):
    await message.answer(
        "🛠 Отправь одну или несколько ссылок (до 50 штук), и я их сокращу через VK.cc.\n"
        "После каждой ссылки жми Enter.\n\n"
        "Пример:\nhttps://site.ru\nhttps://example.com"
    )

# Обработка текста-ссылок
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

    result = []
    for line in lines:
        if not url_pattern.match(line):
            result.append(f"❌ `{line}` — не ссылка")
            continue

        short = await shorten_vk_link(line)
        if short:
            result.append(f"✅ [{line}]({short})")
        else:
            result.append(f"⚠️ `{line}` — ошибка при сокращении")

    # Кол-во успехов
    success_count = sum(1 for r in result if r.startswith("✅"))

    header = f"📊 Сокращено: {success_count}/{len(lines)}\n\n"
    await send_long_message(message, header + "\n\n".join(result))

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
