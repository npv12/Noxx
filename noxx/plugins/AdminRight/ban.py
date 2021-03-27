from pyrogram import Client, filters
import asyncio
from ...noxx import Noxx
from ..constants import HANDLING_KEY
from .kick import check_kick

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("ban", HANDLING_KEY))
async def ban(app: Noxx, message):
    await message.edit("`Banning the user`")

    chat_id = message.chat.id
    user_id = message.from_user.id
    can_kick = True

    #If the user cannot ban people then skip it :)
    if message.chat.type not in ["supergroup", "channel", "group"]:
        await message.edit("`How do you plan on banning a user in his PM?`")
        await asyncio.sleep(2)
        await message.delete()
        return
        
    if(not await check_kick(app,message)):
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
            await app.kick_chat_member(chat_id, reply_to_user_id)
            await message.edit(f"`User banned successfully`")
            await asyncio.sleep(2)
            await message.delete()
        except Exception as error:
            check_status = await app.get_chat_member(
                chat_id=chat_id,
                user_id=reply_to_user_id
            )
            if (check_status.status in ["creator","administrator"]):
                await message.edit(f"`You can't ban an admin`")
                await asyncio.sleep(2)
                await message.delete()
                return
            print(error)
            await message.edit(f"`Something went wrong`")
            await asyncio.sleep(2)
            await message.delete()
    else:
        await message.edit("`Reply to a user to ban`")
        await asyncio.sleep(2)
        await message.delete()
