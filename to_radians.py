from dotenv import load_dotenv
import json
import os
from pymongo import MongoClient
import math

load_dotenv()

client = MongoClient(os.environ.get("MONGO_URL"))
db = client.main
tours = db.tours


def to_radians(string):
    print(string[:100])
    print(string[-100:])
    data = json.loads(string)
    
    for i in range(len(data)):
        print(data[i], len(data[i]))
        break
        for j in range(4, 10):
            data[i][j] *= math.pi / 180
    return json.dumps(data)


for tour in tours.find({}):
    new_data = to_radians(tour["text"]["readings"])
    tours.find_one_and_update({"_id": tour._id}, {"$set": {"text": {"readings": new_data}}} )
