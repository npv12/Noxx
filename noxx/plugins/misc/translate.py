from google_trans_new import google_translator
from pyrogram import filters
from inspect import getfullargspec
from pyrogram.types import Message
from ...noxx import Noxx
import asyncio
from ..constants import HANDLING_KEY

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command(['tr','translate'], HANDLING_KEY))
async def translate(app:Noxx, message):
    await message.edit("Translating...")
    if message.reply_to_message and (message.reply_to_message.text or message.reply_to_message.caption):
        if len(message.text.split()) == 1:
            lang = 'en'
        else:
            lang = message.text.split()[1]
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        detected_language = google_translator().detect(text)
        try:
            translated_text = google_translator().translate(text, lang_tgt=lang)
        except ValueError as err:
            await message.edit(f"Error: `{str(err)}`")
            await asyncio.sleep(2)
            await message.delete()
            return
    else:
        if len(message.text.split()) <= 1:
            await message.edit(f"Specify a language and a text in the order. Alternatively reply to a text")
            await asyncio.sleep(2)
            await message.delete()
            return
        lang = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]
        detected_language = google_translator().detect(text)
        try:
            translated_text = google_translator().translate(text, lang_tgt=lang)
        except ValueError as error:
            await message.edit(f"Unexpected error occured. Try again later")
            await asyncio.sleep(2)
            await message.delete()
            print(error)
            return

    await message.edit(f"Translated from `{detected_language[0]}` to `{lang}`:\n```{translated_text}```")
    