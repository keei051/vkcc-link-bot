from os import environ

BOT_TOKEN = environ.get("BOT_TOKEN")
VK_TOKEN = environ.get("VK_TOKEN")

if not BOT_TOKEN or not VK_TOKEN:
    raise ValueError("Необходимо указать BOT_TOKEN и VK_TOKEN в переменных окружения.")
