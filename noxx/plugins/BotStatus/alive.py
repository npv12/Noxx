from ..constants import HANDLING_KEY
from pyrogram import filters

from ...noxx import Noxx



@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("alive", HANDLING_KEY))
def alive(app: Noxx, message):
    message.edit_text("`Noxx is alive!`")
