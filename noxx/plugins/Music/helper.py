import os
from pytgcalls import GroupCall
import ffmpeg

from .vc import voice_chat

HOME_DIR = os.path.abspath(os.path.expanduser('')) + '/noxx/downloads'

async def download_audio(message):
    group_call = voice_chat.group_call
    client = group_call.client
    raw_file = os.path.join(f'{HOME_DIR}',f"{message.audio.file_unique_id}.raw")
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

async def skip_current_playing():
    group_call = voice_chat.group_call
    playlist = voice_chat.playlist
    if not playlist:
        return
    if len(playlist) == 1:
        voice_chat.is_playing = False
        voice_chat.current = None
        return

    client = group_call.client
    group_call.input_filename = os.path.join(
        HOME_DIR,
        f"{playlist[1].audio.file_unique_id}.raw"
    )

    old_track = playlist.pop(0)
    print(f"- START PLAYING: {playlist[0].audio.title}")
    os.remove(os.path.join(
        HOME_DIR,
        f"{old_track.audio.file_unique_id}.raw")
    )

    if len(playlist) == 1:
        return

    voice_chat.current = playlist[0].audio.title
    await download_audio(playlist[1])
