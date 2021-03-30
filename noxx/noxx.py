from configparser import ConfigParser
import os
from pyrogram import Client
from noxx import API_ID, API_HASH, USERBOT_SESSION

from . import __version__

class Noxx(Client):
    def __init__(self):
        config_file = "noxx.ini"
        name = "noxx"
        config = ConfigParser()
        config.read(config_file)

        plugins = dict(root="noxx/plugins")
        print(USERBOT_SESSION)
        super().__init__(
            USERBOT_SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            plugins=dict(root=f"{name}/plugins"),
            workdir="./",
            app_version=f"Noxx v{__version__}",
        )

    def start(self):
        super().start()
        print(f"Noxx is running. Version is v{__version__}")

    def stop(self):
        super().stop()
        print("I am off to sleep now")

def get_config_var(identifier):
    config_file = "noxx.ini"
    config = ConfigParser()
    config.read(config_file)
    try:
        return config.get('pyrogram', identifier)
    except AttributeError:
        return None
