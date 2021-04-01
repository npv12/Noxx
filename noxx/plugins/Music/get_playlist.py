import os
import asyncio
from pyrogram import filters
from pytgcalls import GroupCall


from .helper import download_audio
from .vc import voice_chat
from ..constants import HANDLING_KEY
from ...noxx import Noxx

#Pyrogram
@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("playlist", HANDLING_KEY))
async def show_playlist(app: Noxx, message):
    playlist = voice_chat.playlist
    if not voice_chat.is_playing:
        await message.edit("No song is being played")
        return

    output = "Playlist is\n"
    c = 1
    for i in playlist:
        output += f"{c}. {i.audio.title}\n"
        c += 1
    await message.edit(output)
