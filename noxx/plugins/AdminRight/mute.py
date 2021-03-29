from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
import re
from time import time
import asyncio
from ...noxx import Noxx
from ..constants import HANDLING_KEY
from .kick import check_kick

unmute_permission = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_stickers=True,
    can_send_animations=True,
    can_send_games=True,
    can_use_inline_bots=True,
    can_add_web_page_previews=True,
    can_send_polls=True,
    can_change_info=True,
    can_invite_users=True,
    can_pin_messages=True,
)

def time_for_mute(temp):
    time_to_mute = -1
    if(temp[2] == 'D' or temp[2] == 'd'):
        time_to_mute = int(temp[1]) * 60 * 60 * 24
    elif(temp[2] == 'H' or temp[2] == 'h'):
        time_to_mute = int(temp[1]) * 60 * 60
    else:
        time_to_mute = int(temp[1]) * 60
    return (time_to_mute)

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("mute", HANDLING_KEY))
async def mute(app: Noxx, message):
    chat_id = message.chat.id
    user_id = -1

    if not await check_kick(app,message):
        await message.edit("You do not have enough rights")
        await asyncio.sleep(2)
        await message.delete()
        return

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id

    elif len(message.command) > 1:
        user_id = message.command[1]

    else:
        await message.edit("Reply to a user to mute")
        await asyncio.sleep(2)
        await message.delete()
        return

    time_to_mute = -1

    if(message.reply_to_message and len(message.command)>1):
        temp = re.split('(\d+)', message.command[1])
        time_to_mute = time_for_mute(temp)
    elif(len(message.command)>2):
        temp = re.split('(\d+)', message.command[2])
        time_to_mute = time_for_mute(temp)

    if(time_to_mute == -1):
        await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
        await message.edit(f"{message.reply_to_message.from_user.first_name} has been muted indefinately.")
        return

    user = await app.get_users(user_id)
    await app.restrict_chat_member(chat_id, user_id, ChatPermissions(), int(time() + time_to_mute))
    await message.edit(f"{user.first_name} has been muted for {time_to_mute}s.")
    return

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("unmute", HANDLING_KEY))
async def unmute(app: Noxx, message):
    chat_id = message.chat.id
    user_id = -1

    if not await check_kick(app,message):
        await message.edit("You do not have enough rights")
        await asyncio.sleep(2)
        await message.delete()
        return

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id

    elif len(message.command) > 1:
        user_id = message.command[1]

    else:
        await message.edit("Reply to a user to mute")
        await asyncio.sleep(2)
        await message.delete()
        return

    user = await app.get_users(user_id)

    await app.restrict_chat_member(chat_id, user_id, permissions = unmute_permission)
    await message.edit(f"{user.first_name} has been unmuted.")
    return
