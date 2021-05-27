from configparser import ConfigParser
from noxx import API_ID, API_HASH, USERBOT_SESSION, BOT_TOKEN
from pyrogram import Client
from pyrogram.parser import parser
import os

from . import __version__

slave = Client('Noxx-help', 
                api_id=API_ID, 
                api_hash=API_HASH, 
                bot_token=BOT_TOKEN, 
                plugins={'root': os.path.join(__package__, 'help-plugins')}
            )

class Noxx(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        config_file = f"{name}.ini"

        config = ConfigParser()
        config.read(config_file)

        plugins = dict(root=f"{name}/plugins")
        super().__init__(
            session_name=name,
            api_id=API_ID,
            api_hash=API_HASH,
            app_version=f"Noxx v{__version__}",
            workdir=".",
            config_file=config_file,
            workers=8,
            plugins=plugins,
        )

    def start(self):
        super().start()
        slave.start()
        print(f"Noxx is running. Version is v{__version__}")

    def stop(self):
        super().stop()
        slave.stop()
        print("I am off to sleep now")
