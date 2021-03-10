from pyrogram import Client, filters
import asyncio
from time import time
from ...noxx import Noxx
from ..constants import HANDLING_KEY

TG_MAX_SELECT_LEN = 100

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("unban", HANDLING_KEY))
async def unban(app: Noxx, message):
    await message.edit("`Unbanning`")

    chat_id = message.chat.id
    user_id = message.from_user.id
    can_kick = True

    #If the user cannot unban people then skip it :)
    if message.chat.type not in ["supergroup", "channel", "group"]:
        await message.edit("`You need to unblock not unban you retard`")
        await asyncio.sleep(2)
        await message.delete()
        return 
    check_status = await app.get_chat_member(
        chat_id=chat_id,
        user_id=user_id
    )
    if (check_status.can_restrict_members == None):
            can_kick=False

    if(not can_kick):
        await message.edit("`You can't unban people in this group`")
        await asyncio.sleep(2)
        await message.delete()
        return 
    
    is_user_info_given = False
    if (len(message.command)>1):
        reply_to_user_id = (await app.get_users(message.command[1])).id
        is_user_info_given = True
    elif (message.reply_to_message):
        reply_to_user_id = message.reply_to_message.from_user.id
        is_user_info_given = True
    if is_user_info_given:
        try:
            await app.unban_chat_member(chat_id, reply_to_user_id)
            await message.edit(f"`User unbanned successfully`")
            await asyncio.sleep(2)
            await message.delete()
        except Exception as error:
            print(error)
            await message.edit(f"`Something went wrong`")
            await asyncio.sleep(2)
            await message.delete()
    else:
        await message.edit("`Reply to a user to unban`")
        await asyncio.sleep(2)
        await message.delete()