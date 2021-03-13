import asyncio
from pyrogram import filters
from pyrogram.types import Message
import requests, json 

from ...noxx import Noxx
from ..constants import HANDLING_KEY

@Noxx.on_message(filters.command(["neko"], HANDLING_KEY) & filters.me)
async def neko(app: Noxx, message: Message):
    message_text = message.reply_to_message.text
    await message.edit("Pasting...")
    try:
        response = requests.post("https://nekobin.com/api/documents", data={"content": message_text}, timeout=3)
        key = (response.json())["result"]["key"]
    except Exception:
        await message.edit_text("`Pasting failed`")
        await asyncio.sleep(2)
        await message.delete()
        return
    else:
        await message.edit(f"Copied to to **Nekobin** : https://nekobin.com/{key}", disable_web_page_preview=True)
        

@Noxx.on_message(filters.command(["dneko"], HANDLING_KEY) & filters.me)
async def dneko(app: Noxx, message: Message):
    message_text = message.reply_to_message.text
    await message.edit("Pasting...")
    try:
        response = requests.post("https://nekobin.com/api/documents", data={"content": message_text}, timeout=3)
        key = (response.json())["result"]["key"]
    except Exception:
        await message.edit_text("`Pasting failed`")
        await asyncio.sleep(2)
        await message.delete()
        return
    else:
        await message.edit(f"Copied to to **Nekobin** : https://nekobin.com/{key}", disable_web_page_preview=True)
        await message.reply_to_message.delete()
        