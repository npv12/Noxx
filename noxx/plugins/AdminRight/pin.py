from pyrogram import Client, filters
import asyncio
from ...noxx import Noxx
from ..constants import HANDLING_KEY

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command(["pin", "unpin"], HANDLING_KEY))
async def pinmessages(app: Noxx, message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        command = f'{HANDLING_KEY}pin'

        if message.chat.type not in ["supergroup", "channel", "group"]:
            message_id = message.reply_to_message.message_id
            if(message.command[0]==command):
                await app.pin_chat_message(chat_id,message_id)
            else:
                await app.unpin_chat_message(chat_id,message_id)
            await message.delete()
            return

        check_status = await app.get_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )

        if message.reply_to_message:
            if (check_status.status in ['creator', 'administrator']):
                message_id = message.reply_to_message.message_id
                if(message.command[0]==command):
                    await app.pin_chat_message(chat_id,message_id)
                else:
                    await app.unpin_chat_message(chat_id,message_id)
                await message.delete()
                return
            else:
                await message.edit("You are not an admin here :(")
                await asyncio.sleep(2)
                await message.delete()
        else:
            await message.edit("Reply to a message to pin")
            await asyncio.sleep(2)
            await message.delete()
    except Exception as e:
        print(e)
        await message.edit("Failed to find the song")
        await asyncio.sleep(2)
        await message.delete()
