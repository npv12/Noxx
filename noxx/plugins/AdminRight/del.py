from pyrogram import Client, filters
import asyncio
from ...noxx import Noxx

@Noxx.on_message(filters.me & filters.command("del", "-"))
async def deletemes(app: Noxx, message):
    await message.edit("`Purging`")

    can_delete = True

    chat_id = message.chat.id
    user_id = message.from_user.id

    #If the user cannot delete message then skip it :)
    if message.chat.type in ["supergroup", "channel", "group"]:
        check_status = await app.get_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )
        if (check_status.can_delete_messages == None):
            can_delete=False

    if(not can_delete):
        await message.edit("You can't delete messages in this group")
        await asyncio.sleep(2)
        await message.delete()
        return 

    if message.reply_to_message:
        del_message = message.reply_to_message
        await del_message.delete()
        


    await message.edit("`Message deleted`")
    await asyncio.sleep(2)
    await message.delete()