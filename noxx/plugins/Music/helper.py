import os
from pytgcalls import GroupCall
import ffmpeg

from .vc import voice_chat

async def download_audio(message):
    home_dir = os.path.abspath(os.path.expanduser(''))
    home_dir += '/noxx/downloads'
    group_call = voice_chat.group_call
    client = group_call.client
    raw_file = os.path.join(f'{home_dir}',f"{message.audio.file_unique_id}.raw")
    if not os.path.isfile(raw_file):
        print("Downloading")
        original_file = await message.download()
        print(original_file)
        print("Download complete, converting now")
        print(raw_file)
        ffmpeg.input(original_file).output(
            raw_file,
            format='s16le',
            acodec='pcm_s16le',
            ac=2,
            ar='48k',
            loglevel='error'
        ).overwrite_output().run()
        os.remove(original_file)
