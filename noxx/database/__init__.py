
import pymongo
from ..noxx import get_config_var

MONGO_URL = get_config_var('mongo_url')
DB_NAME = get_config_var('db_name') or 'Noxx'

def init():
    client = pymongo.MongoClient(MONGO_URL)
    db = client[DB_NAME]
    return db
