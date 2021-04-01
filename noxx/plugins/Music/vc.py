from pytgcalls import GroupCall

class VoiceChatMusic(object):
    def __init__(self):
        self.group_call = GroupCall(None, path_to_log_file='')
        self.chat_id = None
        self.is_playing = False
        self.playlist = []
        self.current = ""

voice_chat = VoiceChatMusic()
