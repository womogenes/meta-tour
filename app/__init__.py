from flask import Flask, send_from_directory, request, flash, redirect, render_template
from werkzeug.utils import secure_filename
import os
from flask_socketio import SocketIO
from dotenv import load_dotenv
from pprint import pprint
import logging
from hashlib import sha256
from uuid import uuid4
import datetime as dt

from database import get_map, add_map

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

app = Flask(__name__,
            static_url_path="",
            static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["PORT"] = int(os.environ.get("PORT"))
socketio = SocketIO(app)


# File uploads
ALLOWED_EXTENSIONS = {"webm", "mp4", "png"}
app.config["UPLOAD_FOLDER"] = "./uploads"


@app.route("/")
def main_page():
    """Serve main page"""
    return render_template("index.html")



@app.route("/maps")
def show_maps():
    """
    List all the maps.
    """
    return render_template("all-maps.html")


@app.route("/maps/<map_id>")
def show_single_map(map_id):
    """
    Show one specific map.
    """
    user_map = get_map(map_id)
    del user_map["_id"]
    return render_template("single-map.html", user_map=user_map)



def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload-data", methods=["POST"])
def upload_data():
    # Data processing will go here, but for now,
    #   there's just print statements for debugging.

    map_id = str(uuid4())
        
    print(f"\n\n=== RECEIVED DATA FROM {request.remote_addr} at {dt.datetime.now()} ===")
    print("**Data fields**")
    print(request.files.to_dict())
    
    print()
    print("**Text fields**")
    pprint(request.form.to_dict())

    print()
    print(f"User ID: {map_id}")

    add_map(request.form.to_dict(), map_id)

    return redirect(f"/maps/{map_id}", code=302)



if __name__ == "__main__":
    logging.getLogger("socketio").setLevel(logging.ERROR)
    logging.getLogger("engineio").setLevel(logging.ERROR)
    logging.getLogger("eventlet").setLevel(logging.ERROR)
    logging.getLogger("eventletwebsocket.handler").setLevel(logging.ERROR)

    if os.environ.get("HTTPS") == "on":
        ssl_context = {
            "certfile": os.path.abspath("static/server.crt"),
            "keyfile": os.path.abspath("static/server.key")
        }
    else:
        ssl_context = dict()

    socketio.run(app, debug=True, host="0.0.0.0", log_output=False, **ssl_context)
