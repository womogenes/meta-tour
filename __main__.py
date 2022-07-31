import os
from app.config import app, socketio

if os.environ.get("HTTPS") == "on":
    ssl_context = {
        "certfile": os.path.abspath("app/static/server.crt"),
        "keyfile": os.path.abspath("app/static/server.key")
    }
else:
    ssl_context = dict()

PORT = int(os.environ.get("PORT"))

socketio.run(app, host="0.0.0.0", **ssl_context, port=PORT, log_output=False, debug=True)
