import datetime as dt
import requests
import base64
from dotenv import load_dotenv
from pymongo import MongoClient
import shutil
import os
import json
import cv2
import time

# from .config import socketio
import sys
sys.path.append("./app/libs/image_stitcher")
from imageStitch import videoToPanorama

load_dotenv()

client = MongoClient(os.environ.get("MONGO_URL"))
db = client.main
tours = db.tours
print(f"Connected to database!")


def add_tour(text_data, raw_file_data, tour_id):
    """
    Processes user input and uploading to the database.
    This really shouldn't go in the database file 😳
    """
    creation_time = dt.datetime.now()

    print(f"=== Processing data from {tour_id} ===")

    file_data = {}
    for file in raw_file_data:

        video_path = os.path.abspath(
            f"./app/uploads/{tour_id}/{file}/source.webm")
        gyro_data = json.loads(text_data["readings"])

        if True:  # try:
            # Extract the first frame
            print(f"  - Processing {file} ... this might take a while.")
            start_time = time.time()

            image = videoToPanorama(gyro_data, video_path, 1)
            retval, buffer = cv2.imencode(".jpg", image)

            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": os.environ.get("IMGBB_KEY"),
                "image": base64.b64encode(buffer),
            }
            try:
                res = requests.post(url, payload)
                img_url = res.json()["data"]["url"]
                file_data[file] = img_url
            except:
                print("uh oh:", res)
                print(res.json())

            print(
                f"     Finished processing in {round(time.time() - start_time)} seconds.")

        else:  # except:
            print(f"")
            continue

    # Delete everything
    if os.environ.get("CLEAR_DATA") == "true":
        shutil.rmtree(f"./app/uploads/{tour_id}")

    title = text_data["title"]
    description = text_data["description"]
    del text_data["title"]
    del text_data["description"]

    document = {
        "tour_id": tour_id,
        "title": title,
        "description": description,
        "timestamp": creation_time,
        "files": file_data,
        "text": text_data
    }
    tours.insert_one(document)

    #socketio.emit('loaded', tour_id, broadcast=True)


def get_tour(tour_id):
    return tours.find_one({"tour_id": tour_id})
