from ..constants import HANDLING_KEY
from pyrogram import filters
from pytgcalls import GroupCall
import asyncio

from ...noxx import Noxx
from .vc import voice_chat

#Pyrogram
@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("leavevc", HANDLING_KEY))
async def leave_vc(app: Noxx, message):
    await message.edit("`Noxx is going away!! Ciao`")
    group_call = voice_chat.group_call
    await group_call.stop()
