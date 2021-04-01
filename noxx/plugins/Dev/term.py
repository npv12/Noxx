import traceback
import sys
import os
import re
import subprocess
from io import StringIO
from pyrogram import filters

from ...noxx import Noxx
from ..constants import HANDLING_KEY


@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("term", HANDLING_KEY))
async def terminal(app:Noxx, message):
    status_message = await message.reply_text("Running")
    if len(message.text.split()) == 1:
        await status_message.edit(f"Usage: `{HANDLING_KEY}term echo owo`")
        return
    args = message.text.split(None, 1)
    teks = args[1]
    if "\n" in teks:
        code = teks.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
            except Exception as err:
                print(err)
                await status_message.edit(
                    """
**Error:**
```{}```
""".format(
                        err
                    )
                )
            output += "**{}**\n".format(code)
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", teks)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb
            )
            await status_message.edit("""**Error:**\n```{}```""".format("".join(errors)))
            return
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await app.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.message_id,
                caption="`Output file`",
            )
            os.remove("output.txt")
            return
        await status_message.edit(f"**Output:**\n```{output}```", parse_mode="markdown")
    else:
        await status_message.edit("**Output:**\n`No Output`")

#Thank you https://github.com/okay-retard/ZectUserBot/blob/master/Zect/modules/dev.py
