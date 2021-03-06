import asyncio
import os
from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import MessageIdInvalid


from ..constants import HANDLING_KEY, POSSIBLE_MEDIA
from .progress import progress_callback
from ...noxx import Noxx


@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command(["download","dl"], HANDLING_KEY))
async def download(app: Noxx, message):
    home_dir = os.path.abspath(os.path.expanduser(' '.join(message.command[1:]) or './'))
    await message.edit("`Downloading`")
    if os.path.isdir(home_dir):
        home_dir = os.path.join(home_dir, 'Dumpster/')
    downloadable_message = None
    if(message.reply_to_message):
        for i in POSSIBLE_MEDIA:
            if getattr(message.reply_to_message, i, None):
                home_dir = os.path.join(home_dir, f"{i}/")
                downloadable_message = message.reply_to_message
                break
    else:
        for i in POSSIBLE_MEDIA:
            if getattr(message, i, None):
                downloadable_message = message
                break

    await download_helper_tg(message, downloadable_message, home_dir)

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command(["silentdownload","sdl"], HANDLING_KEY))
async def silent_download(app: Noxx, message):
    home_dir = os.path.abspath(os.path.expanduser(' '.join(message.command[1:]) or './'))
    saved_message = await app.send_message("me", 'Downloading')
    await saved_message.edit("`Downloading`")
    if os.path.isdir(home_dir):
        home_dir = os.path.join(home_dir, 'Dumpster/')
    downloadable_message = None
    if(message.reply_to_message):
        for i in POSSIBLE_MEDIA:
            if getattr(message.reply_to_message, i, None):
                home_dir = os.path.join(home_dir, f"{i}/")
                downloadable_message = message.reply_to_message
                break
    else:
        for i in POSSIBLE_MEDIA:
            if getattr(message, i, None):
                downloadable_message = message
                break
    await message.delete()
    await download_helper_tg(saved_message, downloadable_message, home_dir)

#message is the message which is edited to show the realtime status. downloadable_message is the message which contains the file
async def download_helper_tg(message, downloadable_message, home_dir):
    if(downloadable_message == None):
        await message.edit("This is not a valid media")
    else:
        try:
            text = 'Downloading your file....\n'
            try:
                home_dir = await downloadable_message.download(home_dir, progress=progress_callback, progress_args=(message, text, False))
            except:
                await message.edit("Some error occured! Try again later")
                return
            await message.edit(f"Download complete. Saved to `{home_dir}`")
        except MessageIdInvalid:
            await message.reply_text('Download cancelled!')
        return
