import os
from app import app, socketio

if os.environ.get("HTTPS") == "on":
    ssl_context = {
        "certfile": os.path.abspath("static/server.crt"),
        "keyfile": os.path.abspath("static/server.key")
    }
else:
    ssl_context = dict()

socketio.run(app, debug=True, host="0.0.0.0", log_output=False, **ssl_context)
