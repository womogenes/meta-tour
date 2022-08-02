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
import numpy as np

# from .config import socketio
import sys
sys.path.append("./app/libs")
from imageStitch import videoToPanorama
from trace_position import trace_position, twoD_trace_map

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

        try:
            print(f"  - Processing {file} ... this might take a while.")
            start_time = time.time()

            image = videoToPanorama(gyro_data, video_path, 1)
            if image == 1:
                raise ValueError()

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

        except:
            print(f"Some error occurred :(")
            continue

    # Delete everything
    if os.environ.get("CLEAR_DATA") == "true":
        shutil.rmtree(f"./app/uploads/{tour_id}")

    # Generate trace map
    position = trace_position(np.asarray(json.loads(text_data["readings"])))
    image = twoD_trace_map(position)
    retval, buffer = cv2.imencode(".jpg", image)
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": os.environ.get("IMGBB_KEY"),
        "image": base64.b64encode(buffer),
    }
    res = requests.post(url, payload)
    tracemap_url = res.json()["data"]["url"]

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
        "text": text_data,
        "tracemap_url": tracemap_url
    }
    tours.insert_one(document)

    #socketio.emit('loaded', tour_id, broadcast=True)


def get_tour(tour_id):
    return tours.find_one({"tour_id": tour_id})
