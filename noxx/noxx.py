from configparser import ConfigParser

from pyrogram import Client

from . import __version__


class Noxx(Client):
    def __init__(self):
        config_file = "noxx.ini"

        config = ConfigParser()
        config.read(config_file)

        plugins = dict(root="noxx/plugins")
        super().__init__(
            session_name="noxx",
            app_version=f"Noxx v{__version__}",
            workdir=".",
            config_file=config_file,
            workers=8,
            plugins=plugins,
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
