from itranslate import itranslate as itrans
from pyrogram import filters
from ...noxx import Noxx
import asyncio
from ..constants import HANDLING_KEY

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command(['tr','translate'], HANDLING_KEY))
async def translate(app:Noxx, message):
    await message.edit("Translating...")
    text = ''
    lang = 'en'
    if message.reply_to_message and (message.reply_to_message.text or message.reply_to_message.caption):
        # Detect which language to translate to. Defaults to english
        if len(message.text.split()) != 1:
            lang = message.text.split()[1]
        
        # Detect the text for translation
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        
        
    else:
        if len(message.text.split()) <= 1:
            await message.edit(f"Specify a language and a text in the order. Alternatively reply to a text")
            await asyncio.sleep(2)
            await message.delete()
            return
        lang = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]

    try:
        translated_text = itrans(text, to_lang=lang)
    except ValueError as err:
        await message.edit(f"Error: `{str(err)}`")
        await asyncio.sleep(2)
        await message.delete()
        return

    await message.edit(f"Translated to `{lang}`:\n```{translated_text}```")
    