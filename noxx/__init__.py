from configparser import ConfigParser
import os
from sys import version_info

__version__ = "1.1"
NAME = 'noxx'

if version_info[:2] < (3, 6):
    print("Noxx needs version 3.6 or more")
    quit()

print("Setting up ENV")
ENV = bool(os.environ.get('ENV', False))

if ENV:
    # Pyrogram details
    API_ID = os.environ.get("API_ID", None)
    API_HASH = os.environ.get("API_HASH", None)
    USERBOT_SESSION = os.environ.get("USERBOT_SESSION", None)

else:
    #Config File
    config_file = "noxx.ini"
    config = ConfigParser()
    config.read(config_file)

    # Pyrogram details
    API_ID = config.get(NAME, 'API_ID')
    API_HASH = config.get(NAME, "API_HASH")
    USERBOT_SESSION = config.get(NAME, "USERBOT_SESSION")

print("Env set properly")