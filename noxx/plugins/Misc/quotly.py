
from pyrogram import filters

from ...noxx import Noxx
from ..constants import HANDLING_KEY

BOT = '@QuotLyBot'

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command(['q','quote'], HANDLING_KEY))
async def q_maker(app:Noxx, message):
    chat_id = message.chat.id
    await message.edit("Making it into a quote :D")
    if not message.reply_to_message:
        await message.edit("**Reply a message with text.**")
        return
    await message.reply_to_message.forward(BOT)
    is_sticker = False
    while not is_sticker:
        x = await get_response(app)
        if(x.sticker):
            await x.forward(chat_id)
            is_sticker=True
            await message.delete()

async def get_response(app:Noxx):
    async for x in app.iter_history(BOT, limit=1):
        return x
