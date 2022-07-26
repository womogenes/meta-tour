from flask import Flask, send_from_directory, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from flask_socketio import SocketIO
from dotenv import load_dotenv
from pprint import pprint
import logging
from hashlib import sha256

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

app = Flask(__name__,
            static_url_path="",
            static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
socketio = SocketIO(app)


# File uploads
ALLOWED_EXTENSIONS = {"webm", "mp4", "png"}
app.config["UPLOAD_FOLDER"] = "./uploads"

@app.route("/")
def main_page():
    """Serve main page"""
    return send_from_directory("static", "index.html")

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("download_file", name=filename))


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

    socketio.run(app, debug=True, port=5000, host="0.0.0.0", log_output=False, **ssl_context)
