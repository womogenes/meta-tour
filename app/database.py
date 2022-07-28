import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ.get("MONGO_URL"))
db = client.main
tours = db.tours


def add_tour(data, user_id):
    document = {
        "tour_id": user_id,
        "data": data
    }
    tours.insert_one(document)


def get_tour(user_id):
    return tours.find_one({ "tour_id": user_id })
