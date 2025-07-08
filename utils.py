import aiohttp
import logging
import re
from config import VK_TOKEN

url_pattern = re.compile(r"https?://[^\s]+")

def is_valid_url(text: str) -> bool:
    return bool(url_pattern.match(text))

def escape_md(text: str) -> str:
    special_chars = r'_*[]()~`>#+-=|{}.!'
    for ch in special_chars:
        text = text.replace(ch, '\\' + ch)
    return text

async def shorten_vk_link(link: str) -> str | None:
    url = "https://vk.cc/shorten"
    headers = {"Authorization": f"Bearer {VK_TOKEN}"}
    params = {"url": link}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("short_url")
                else:
                    logging.error(f"VK shorten error: status {response.status}")
    except aiohttp.ClientError as e:
        logging.error(f"VK shorten request failed: {e}")
    return None

async def send_long_message(message, text: str, max_length=4096):
    if len(text) <= max_length:
        await message.answer(text, disable_web_page_preview=True)
        return
    parts = [text[i:i + max_length] for i in range(0, len(text), max_length)]
    for part in parts:
        await message.answer(part, disable_web_page_preview=True)
