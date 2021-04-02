from ..constants import HANDLING_KEY
from pyrogram import filters
import asyncio
import html

from ...noxx import Noxx

async def can_promote(app, message):
    can_promote = True
    chat_id = message.chat.id
    user_id = message.from_user.id
    check_status = await app.get_chat_member(
        chat_id=chat_id,
        user_id=user_id
    )
    if check_status.status == 'creator':
        can_promote=True
    elif (check_status.can_promote_members == None):
            can_promote=False

    if(not can_promote):
        await message.edit("`You don't have enough rights`")
        await asyncio.sleep(2)
        await message.delete()
    return can_promote



@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("promote", HANDLING_KEY))
async def promote(app: Noxx, message):
    try:
        chat_id = message.chat.id
        user = None
        title = None

        if message.chat.type not in ["supergroup", "channel", "group"]:
            await message.edit("`How do you plan on promoting a user in his PM?`")
            await asyncio.sleep(2)
            await message.delete()
            return

        if not await can_promote(app, message):
           return

        if message.reply_to_message:
            user = message.reply_to_message.from_user
        elif(len(message.command) == 2 and message.reply_to_message):
            user = message.reply_to_message.user
            title = message.command[1]
        elif len(message.command) == 2:
            user = await app.get_users(message.command[1])
        elif len(message.command) > 2:
            user = await app.get_users(message.command[1])
            title = message.command[2]
        else:
            await message.edit("`Reply to a user or give me his username`")
            await asyncio.sleep(2)
            await message.delete()
            return

        if not await app.promote_chat_member(
            chat_id=chat_id,
            user_id=user.id,
            is_anonymous=False,
            can_change_info=False,
            can_delete_messages=True,
    		can_restrict_members=True,
    		can_invite_users=True,
    		can_pin_messages=True,
    		can_promote_members=False,
    		can_manage_voice_chats=True
        ):
            await message.edit("<code>I cannot promote that.</code>")
            return

        if title and message.chat.type == "supergroup":
            # if they also have a title
            try:
                if not await app.set_administrator_title(
                    chat_id=chat_id,
                    user_id=user.id,
                    title=title
                ):
                    await message.edit(f'<code>User was promoted but I cannot set their title to "{title}"</code>')

            except:
                await message.edit(f'<code>User was promoted but I cannot set their title to "{title}"</code>')
        await message.edit(f'<a href="https://t.me/{user.id}">{user.first_name}</a><code> can now reign too!</code>', disable_web_page_preview=True)

        await asyncio.sleep(2)
        await message.delete()
    except:
        await message.edit("something went wrong")
        await asyncio.sleep(2)
        await message.delete()
