from pyrogram import filters
from pyrogram.types import User, Message
from pyrogram.errors import FloodWait
from time import sleep

from ...noxx import Noxx, get_config_var
from ...database.pmpermit import PmPermit
from ..constants import HANDLING_KEY

PM_PERMIT = get_config_var('pm_permit')
PM_LIMIT = int(get_config_var('pm_limit'))

FIRST_PM_MESSAGE = "`Hi there!! I am Noxx \n\nMy owner hasn't approved you to PM him yet. Please wait till he comes back online.\n\nThank you for your patience`"
WARN_MESSAGE = f"`Repeated messaging him won't help. Also note that you will be blocked if you message him a lot >w<`"

@Noxx.on_message(filters.private & ~filters.me)
async def incoming_pm(app: Noxx, message: Message):
    chat_id = message.chat.id
    if PM_PERMIT:
        approved = PmPermit().is_approved(chat_id)
        blocked = PmPermit().is_blocked(chat_id)

        if approved:
            return

        elif blocked:
            await app.block_user(chat_id)

        elif PmPermit().number_of_messages_sent(chat_id) > PM_LIMIT:
            await app.block_user(chat_id)
            PmPermit().block(chat_id)
        else:
            number_of_messages_sent = PmPermit().number_of_messages_sent(chat_id)
            if(number_of_messages_sent == 0):
                await app.send_message(chat_id, FIRST_PM_MESSAGE)
            elif(number_of_messages_sent == int(PM_LIMIT/2)):
                await app.send_message(chat_id, WARN_MESSAGE)
            PmPermit().increment_message_sent(chat_id)


@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("approve", HANDLING_KEY))
def approve(app: Noxx, message: Message):
    message.edit("`Approving user`")
    PmPermit().approve(message.chat.id)
    message.edit("You have been approved to PM me.")


@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("block", HANDLING_KEY))
def block(app: Noxx, message: Message):
    message.edit("`Blocking user`")
    PmPermit().block_pm(message.chat.id)
    message.edit("`You have been blocked.`")
