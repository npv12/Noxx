import os
import signal
from pyrogram import filters
from ..noxx import Noxx
from .constants import HANDLING_KEY

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("shutdown", HANDLING_KEY))
async def ping(app: Noxx, message):
    await message.edit("Goodbye!")
    os.kill(os.getpid(), signal.SIGINT)
