from ..constants import HANDLING_KEY
from pytgcalls import GroupCall
from pyrogram import filters
import asyncio

from .vc import voice_chat
from .helper import skip_current_playing
from ...noxx import Noxx

#Pyrogram
@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("next", HANDLING_KEY))
async def next_music(app: Noxx, message):
    await message.edit("Playing the next music")
    await skip_current_playing()

#pytgcalls
@voice_chat.group_call.on_playout_ended
async def playout_ended_handler(group_call, filename):
    await skip_current_playing()
