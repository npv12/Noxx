import os
from pyrogram import filters
from pyrogram.types import User, Message
from pyrogram.errors import PeerIdInvalid
import asyncio

from ..noxx import Noxx
from .constants import HANDLING_KEY

#Kanged from https://github.com/okay-retard/ZectUserBot/blob/master/Zect/modules/whois.py

def reply_check(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


infotext = (
    "**[{full_name}](tg://user?id={user_id})**\n"
    " > UserID: `{user_id}`\n"
    " > First Name: `{first_name}`\n"
    " > Last Name: `{last_name}`\n"
    " > Username: @{username}\n"
)


def full_name(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("info", HANDLING_KEY))
async def info(app: Noxx, message):
    try:
        await message.edit("Fetching info")
        cmd = message.command
        if not message.reply_to_message and len(cmd) == 1:
            get_user = message.from_user.id
        elif len(cmd) == 1:
            get_user = message.reply_to_message.from_user.id
        elif len(cmd) > 1:
            get_user = cmd[1]
            try:
                get_user = int(cmd[1])
            except ValueError:
                pass
        try:
            user = await app.get_users(get_user)
        except PeerIdInvalid:
            await message.reply("I don't know that User.")
            return
        pfp = await app.get_profile_photos(user.id)
        if not pfp:
            await message.edit_text(
                infotext.format(
                    full_name=full_name(user),
                    user_id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name or "",
                    username=user.username or "",
                ),
                disable_web_page_preview=True,
            )
        else:
            dls = await app.download_media(pfp[0]["file_id"], file_name=f"{user.id}.png")
            await message.delete()
            await app.send_document(
                message.chat.id,
                dls,
                caption=infotext.format(
                    full_name=full_name(user),
                    user_id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name or "",
                    username=user.username or "",
                ),
                reply_to_message_id=message.reply_to_message.message_id
                if message.reply_to_message
                else None,
            )
            os.remove(dls)
    except:
        await message.edit("something went wrong")
        await asyncio.sleep(2)
        await message.delete()

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.command("id", HANDLING_KEY) & filters.me)
async def id(app: Noxx, message):
    try:
        cmd = message.command
        chat_id = message.chat.id
        if not message.reply_to_message and len(cmd) == 1:
            get_user = message.from_user.id
        elif len(cmd) == 1:
            get_user = message.reply_to_message.from_user.id
        elif len(cmd) > 1:
            get_user = cmd[1]
            try:
                get_user = int(cmd[1])
            except ValueError:
                pass
        try:
            user = await app.get_users(get_user)
        except PeerIdInvalid:
            await message.edit("I don't know that User.")
            return
        text = "**User ID**: `{}`\n**Chat ID**: `{}`".format(user.id, chat_id)
        await message.edit(text)
    except:
        await message.edit("something went wrong")
        await asyncio.sleep(2)
        await message.delete()
