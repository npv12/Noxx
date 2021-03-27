from pyrogram import Client, filters
import asyncio
from ...noxx import Noxx
from ..constants import HANDLING_KEY, TG_MAX_SELECT_LEN
from .purge import fast_purge, slow_purge, check_delete_perm

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command(["del", "d"], HANDLING_KEY))
async def deletemes(app: Noxx, message):
    await message.edit("`Deleting`")

    chat_id = message.chat.id
    user_id = message.from_user.id

    #If the user cannot delete message then skip it :)
    if(not await check_delete_perm(app, message)):
        return

    #check if user replied to a message. or else do nothing
    if message.reply_to_message:
        if (len(message.command)>1):

            #only supergroups have sequential message_id. so currently it will only delete messages in supergroups in more than one number
            if message.chat.type not in ["supergroup", "channel"]:
                await slow_purge(app, message,chat_id, number_of_messages = int(message.command[1]))
                return

            await fast_purge(app, message,chat_id, number_of_messages = int(message.command[1]))

        else:
            #delete a single message if no arg is given
            del_message = message.reply_to_message
            await del_message.delete()

    else:
        await message.edit("`Reply to a message to delete`")
        await asyncio.sleep(2)
        await message.delete()
