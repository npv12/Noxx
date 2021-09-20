import asyncio
from pyrogram import filters
from pyrogram.types import Message
import requests, json 

from ...noxx import Noxx
from ..constants import HANDLING_KEY

@Noxx.on_message(filters.command(["bin"], HANDLING_KEY) & filters.me)
async def neko(app: Noxx, message: Message):
    message_text = message.reply_to_message.text
    await message.edit("Pasting...")
    key = 'a'
    try:
        response = requests.post("https://hastebin.com/documents", data=message_text, timeout=3)
        key = (response.json())["key"]
    except Exception:
        await message.edit_text("`Pasting failed`")
        await asyncio.sleep(2)
        await message.delete()
        return -1
    else:
        await message.edit(f"Copied to to **Hastebin** : https://hastebin.com/{key}", disable_web_page_preview=True)
    return key

@Noxx.on_message(filters.command(["dbin"], HANDLING_KEY) & filters.me)
async def dneko(app: Noxx, message: Message):
    key = await neko(app, message)
    if key != -1:
        await message.reply_to_message.delete()
        