import os
import asyncio
from pyrogram import filters
from pytgcalls import GroupCall


from .helper import download_audio
from .vc import voice_chat
from ..constants import HANDLING_KEY
from ...noxx import Noxx

#Pyrogram
@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("playvc", HANDLING_KEY))
async def play_track(app: Noxx, message):
    await message.edit("`Noxx is going to play music`")
    group_call = voice_chat.group_call
    playlist = voice_chat.playlist

    if not group_call.is_connected:
        await message.edit("No voice chat is active. Enable one and try again")
        await asyncio.sleep(2)
        await message.delete()

    # check audio file is supplied
    if message.audio:
        if message.audio.duration > 600:
            await message.reply_text("`Audio file is too large for Noxx to handle. Noxx doesn't like it this big`")
            return
        audio_message = message
    elif message.reply_to_message and message.reply_to_message.audio:
        audio_message = message.reply_to_message
    else:
        await message.edit("`This is not an audio file!!`")
        await asyncio.sleep(2)
        await message.delete()
        return

    # check already added
    if playlist and playlist[-1].audio.file_unique_id == audio_message.audio.file_unique_id:
        await message.reply_text("`The song is already queued`")
        return

    home_dir = os.path.abspath(os.path.expanduser(''))
    home_dir += '/noxx/downloads'

    # add to playlist
    playlist.append(audio_message)
    voice_chat.is_playing = True

    if len(playlist) == 1:
        reply = await message.reply_text("`Downloading the file to play`")
        await download_audio(playlist[0])
        group_call.input_filename = os.path.join(f'{home_dir}',f"{playlist[0].audio.file_unique_id}.raw")
        await reply.delete()
        print(f"- STARTED PLAYING: {playlist[0].audio.title}")
        voice_chat.current = 0

    #Keep downloaing other music files in the playlist
    for track in playlist[:2]:
        await download_audio(track)
