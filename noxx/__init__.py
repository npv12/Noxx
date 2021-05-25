from sys import version_info
from configparser import ConfigParser
import os

__version__ = "1.0"

if version_info[:2] < (3, 6):
    print("Pyrogram needs version 3.6 or more")
    quit()
ENV = bool(os.environ.get('ENV', False))
print("Setting up ENV")
if ENV:
    # Pyrogram details
    API_ID = os.environ.get("API_ID", None)
    API_HASH = os.environ.get("API_HASH", None)
    USERBOT_SESSION = os.environ.get("USERBOT_SESSION", None)

    # MongoDB details
    MONGO_URL = os.environ.get("MONGO_URL", False)
    DB_NAME = os.environ.get("DB_NAME", "noxx")

    # Get the Values from our .env
    PM_PERMIT = bool(os.environ.get("PM_PERMIT", False))
    PM_LIMIT = int(os.environ.get("PM_LIMIT", None))

    #Downloading files
    DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", None)

    #Weather
    OPENWEATHER_API = os.environ.get("OPENWEATHER_API", None)

    #Stickers
    STICKER_PACK_NAME = os.environ.get("STICKER_PACK_NAME", "Kang_Pack")
else:
    #Config File
    config_file = "noxx.ini"
    config = ConfigParser()
    config.read(config_file)

    # Pyrogram details
    API_ID = config.get("pyrogram", 'api_id')
    API_HASH = config.get("pyrogram", "api_hash")
    USERBOT_SESSION = config.get("pyrogram", "userbot_session")

    # MongoDB details
    MONGO_URL = config.get("pyrogram", "mongo_url")
    DB_NAME = config.get("pyrogram", "db_name")

    # Get the Values from our .env
    PM_PERMIT = bool(config.get("pyrogram", "pm_permit"))
    PM_LIMIT = int(config.get("pyrogram", "pm_limit"))

    #Downloading files
    DOWNLOAD_LOCATION = config.get("pyrogram", "download_location")

    #Weather
    OPENWEATHER_API = config.get("pyrogram", "openweather_api")

    #Stickers
    STICKER_PACK_NAME = config.get("pyrogram", "sticker_pack_name")
print("Env set properly")
