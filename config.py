import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
VK_TOKEN = os.getenv("VK_TOKEN")

# Настройки
MAX_LINKS_PER_BATCH = 50

if not BOT_TOKEN or not VK_TOKEN:
    raise ValueError("BOT_TOKEN или VK_TOKEN не найдены в .env")
