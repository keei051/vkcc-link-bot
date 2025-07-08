import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
VK_TOKEN = os.getenv("VK_TOKEN")

# Ограничения
MAX_LINKS_PER_BATCH = 50  # максимум ссылок за 1 массовую загрузку
