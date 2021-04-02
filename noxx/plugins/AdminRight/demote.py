from ..constants import HANDLING_KEY
from pyrogram import filters
import asyncio
from .promote import can_promote

from ...noxx import Noxx

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("demote", HANDLING_KEY))
async def promote(app: Noxx, message):
    chat_id = message.chat.id
    user_id = None
    title = None
    if message.chat.type not in ["supergroup", "channel", "group"]:
        await message.edit("`How did you even promote a user in his pm`")
        await asyncio.sleep(2)
        await message.delete()
        return

    if not await can_promote(app, message):
       return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) == 2:
        user_id = message.command[1]
    else:
        await message.edit("`Reply to a user or give me his username`")
        await asyncio.sleep(2)
        await message.delete()
        return

    if not await app.promote_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        is_anonymous=False,
        can_manage_chat=False,
		can_change_info=False,
		can_post_messages=False,
		can_edit_messages=False,
		can_delete_messages=False,
		can_restrict_members=False,
		can_invite_users=False,
		can_pin_messages=False,
		can_promote_members=False,
        can_manage_voice_chats=False

    ):
        await message.edit("<code>I cannot demote that.</code>")
        return

    await message.edit(f'<a href="https://t.me/{user_id}">{user_id}</a><code> can no longer be a dictator</code>', disable_web_page_preview=True)

    await asyncio.sleep(2)
    await message.delete()
