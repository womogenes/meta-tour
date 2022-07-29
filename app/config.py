from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os
import logging


logging.getLogger("socketio").setLevel(logging.ERROR)
logging.getLogger("engineio").setLevel(logging.ERROR)
logging.getLogger("eventlet").setLevel(logging.ERROR)
logging.getLogger("eventletwebsocket.handler").setLevel(logging.ERROR)


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

app = Flask(__name__,
            static_url_path="",
            static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["PORT"] = int(os.environ.get("PORT"))
socketio = SocketIO(app)
