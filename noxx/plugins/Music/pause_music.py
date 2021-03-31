from ..constants import HANDLING_KEY
from pyrogram import filters

from .vc import voice_chat
from ...noxx import Noxx

#Pyrogram
@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command(["pause", 'pausemusic'], HANDLING_KEY))
async def join_vc(app: Noxx, message):
    await message.edit("`Noxx is pausing to play`")
    group_call = voice_chat.group_call
    group_call.client = app
    group_call.pause_playout()
    voice_chat.is_playing = False
