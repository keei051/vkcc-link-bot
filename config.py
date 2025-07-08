import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
VK_TOKEN = os.getenv("VK_TOKEN")

if not BOT_TOKEN or not VK_TOKEN:
    raise ValueError("Переменные окружения BOT_TOKEN и VK_TOKEN должны быть заданы в .env")

# Ограничения
MAX_LINKS_PER_BATCH = 50  # Максимум ссылок за одну массовую загрузку
