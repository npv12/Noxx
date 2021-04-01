import os
import html
from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import MessageIdInvalid


from .progress import progress_callback
from ..constants import HANDLING_KEY
from ...noxx import Noxx

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("upload", HANDLING_KEY))
async def upload(app: Noxx, message):
    DIR = os.path.expanduser(' '.join(message.command[1:]))
    if not DIR:
        return
    text = f'Uploading {html.escape(DIR)}... \n'
    reply = await message.edit(text)
    try:
        await app.send_document(chat_id = message.chat.id, document = DIR, progress=progress_callback, progress_args=(reply, text, True), force_document=True, reply_to_message_id=None if message.chat.type in ('private', 'bot') else message.message_id)
    except MessageIdInvalid:
        await message.reply_text('Upload cancelled!')
    else:
        await reply.delete()
