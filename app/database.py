import os
import shutil
from pymongo import MongoClient
from dotenv import load_dotenv
import cv2
import base64
import requests
import numpy as np
import datetime as dt
from flask_socketio import emit

from .config import socketio

load_dotenv()

client = MongoClient(os.environ.get("MONGO_URL"))
db = client.main
tours = db.tours


def extractImages(path_in):
    count = 0
    vidcap = cv2.VideoCapture(path_in)
    vidcap.set(cv2.CAP_PROP_POS_MSEC, 1000)
    success, image = vidcap.read()
    vidcap.release()
    return image


def add_tour(text_data, raw_file_data, tour_id):
    """
    Processes user input and uploading to the database.
    This really shouldn't go in the database file 😳
    """
    creation_time = dt.datetime.now()

    file_data = {}
    for file in raw_file_data:
        video_path = f"./app/uploads/{tour_id}/{file}/source.webm"

        try:
            # Extract the first frame
            image = extractImages(video_path)

            # Do some processing; for now, just real basic and then upload
            image = cv2.rotate(image, cv2.ROTATE_180)
            kernel = np.array([[0, -1, 0],
                               [-1, 5,-1],
                               [0, -1, 0]])
            image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
            retval, buffer = cv2.imencode(".jpg", image)

            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": os.environ.get("IMGBB_KEY"),
                "image": base64.b64encode(buffer),
            }
            res = requests.post(url, payload)
            img_url = res.json()["data"]["url"]
            file_data[file] = img_url

        except:
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
    return tours.find_one({ "tour_id": tour_id })
