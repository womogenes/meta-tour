import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ.get("MONGO_URL"))
db = client.main
maps = db.maps


def add_map(data, user_id):
    document = {
        "map_id": user_id,
        "data": data
    }
    maps.insert_one(document)


def get_map(user_id):
    return maps.find_one({ "map_id": user_id })
