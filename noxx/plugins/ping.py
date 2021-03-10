from pyrogram import Client, filters

from datetime import datetime
from .constants import HANDLING_KEY
from ..noxx import Noxx


@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("ping", HANDLING_KEY))
async def ping(app: Noxx, message):
    start_time = datetime.now()
    await message.edit("Pong!")
    end_time = datetime.now()
    time_taken = (end_time - start_time).microseconds / 1000
    await message.edit(f"`Ping is`\n{time_taken} ms")