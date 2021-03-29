from pyrogram import Client, filters
import asyncio
from ...noxx import Noxx
from ..constants import HANDLING_KEY

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("music", HANDLING_KEY))
async def get_music(app: Noxx, message):
    await message.edit('`Finding ths song`')
    try:
        song_name = ''
        if len(message.command) > 1:
            song_name = ' '.join(message.command[1:])

        elif message.reply_to_message and len(cmd) == 1:
            song_name = (message.reply_to_message.text or message.reply_to_message.caption)

        elif len(message.command) == 1:
            await message.edit('Provide a song name')
            await asyncio.sleep(2)
            await message.delete()
            return

        songs = await app.get_inline_bot_results('SongRefBot',song_name)
        await app.send_inline_bot_result(chat_id=message.chat.id, query_id=songs.query_id, result_id=songs.results[0].id, hide_via=True)
        await message.delete()

    except Exception as e:
        print(e)
        await message.edit("Failed to find the song")
        await asyncio.sleep(2)
        await message.delete()
