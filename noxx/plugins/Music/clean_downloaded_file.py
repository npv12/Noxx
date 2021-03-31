from ..constants import HANDLING_KEY
from pyrogram import filters

from .vc import voice_chat
from .helper import HOME_DIR
from ...noxx import Noxx

#Pyrogram
@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command(["clean",], HANDLING_KEY))
async def clean_vc(app: Noxx, message):
    await message.edit("`Noxx is cleaning the house`")
    count = clean_service()
    await message.edit(f"Cleaning complete. Deleted {count} files")

def clean_service():
    all_files = os.listdir(HOME_DIR)
    for track in voice_chat.playlist[:2]:
        track_file = f"{track.audio.file_unique_id}.raw"
        if track_file in all_files:
            all_files.remove(track_file)
    count = 0
    if all_files:
        for fn in all_files:
            if fn.endswith(".raw"):
                count += 1
                os.remove(os.path.join(HOME_DIR, fn))
    return count
