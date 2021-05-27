from pyrogram import filters, Client

@Client.on_message(filters.me & filters.command("alive", "-"))
async def alive(app, message):
    await message.edit_text("`Noxx is alive!`")