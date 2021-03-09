from pyrogram import filters

from ..noxx import Noxx


@Noxx.on_message(filters.me & filters.command("alive", "-"))
def alive(app: Noxx, message):
    message.edit_text("`Noxx is alive!`")
