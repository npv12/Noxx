from ..constants import HANDLING_KEY
from pytgcalls import GroupCall
from pyrogram import filters
import asyncio

from .vc import voice_chat
from ...noxx import Noxx

#Pyrogram
@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("joinvc", HANDLING_KEY))
async def join_vc(app: Noxx, message):
    await message.edit("`Noxx is joining the voice chat`")
    group_call = voice_chat.group_call
    group_call.client = app
    if group_call.is_connected:
        await message.reply_text("`Noxx is already in the voice chat`")
    else:
        await group_call.start(message.chat.id)
        await message.edit("`Noxx joined :D`")

#pytgcalls
@voice_chat.group_call.on_network_status_changed
async def network_status_changed(group_call: GroupCall, is_connected: bool):
    if is_connected:
        voice_chat.chat_id = int("-100" + str(group_call.full_chat.id))
    else:
        voice_chat.chat_id = None
