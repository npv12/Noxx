from pyrogram import Client, filters

from datetime import datetime
from ..noxx import Noxx


@Noxx.on_message(filters.me & filters.command("ping", "-"))
async def ping(app: Noxx, message):
    start_time = datetime.now()
    await message.edit("Pong!")
    end_time = datetime.now()
    time_taken = (end_time - start_time).microseconds / 1000
    await message.edit(f"`Ping is`\n{time_taken} ms")