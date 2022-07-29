from flask import Flask, send_from_directory, request, flash, redirect, render_template
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from pprint import pprint
import logging
from hashlib import sha256
from uuid import uuid4
import datetime as dt
from threading import Thread

from .database import get_tour, add_tour, tours
from .config import app

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


# File uploads
ALLOWED_EXTENSIONS = {"webm", "mp4", "png"}
app.config["UPLOAD_FOLDER"] = "./uploads"


@app.route("/")
def main_page():
    """Serve main page"""
    return render_template("index.html")


@app.route("/capture")
def capture_page():
    return render_template("capture.html")


@app.route("/tours")
def show_tours():
    """
    List all the tours.
    """
    all_tours = list(tours.find({}))
    return render_template("all-tours.html", tours=all_tours)


@app.route("/tours/<tour_id>")
def show_single_tour(tour_id):
    """
    Show one specific tour.
    """
    tour = get_tour(tour_id)
    return render_template("single-tour.html", tour=tour)



def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload-data", methods=["POST"])
def upload_data():
    # Data processing will go here, but for now,
    #   there's just print statements for debugging.

    tour_id = str(uuid4())
        
    print(f"\n\n=== RECEIVED DATA FROM {request.remote_addr} at {dt.datetime.now()} ===")
    print("**Data fields**")
    print(request.files.to_dict())
    
    print()
    print("**Text fields**")
    pprint(request.form.to_dict())

    print()
    print(f"User ID: {tour_id}")

    # Save the files immediately
    raw_file_data = request.files.to_dict()
    for file in raw_file_data:
        os.makedirs(f"./app/uploads/{tour_id}/{file}")
        video_path = f"./app/uploads/{tour_id}/{file}/source.webm"
        raw_file_data[file].save(video_path)
        raw_file_data[file].close()

    thread = Thread(target=add_tour, args=(request.form.to_dict(), request.files.to_dict(), tour_id))
    thread.start()

    return redirect(f"/tours/{tour_id}", code=302)
