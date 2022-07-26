# Final project server

## Development setup

Requires Python 3.9 (3.10 breaks everything for some reason), along with the following libraries:

- [Flask](https://flask.palletsprojects.com/en/2.1.x/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/intro.html)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [eventlet](https://eventlet.net/)

All of these are included in `requirements.txt`, so to install all dependencies simply do

```
pip install -r requirements.txt
```

Optional: for development, set up a `.env` file that looks like this

```
SECRET_KEY=<some random string>
ENV=development
```

To start the server, run `python server.py`.

### Production

Not entirely figured out yet, but there's currently a Heroku app running this with gunicorn at https://meta-tour.herokuapp.com.

## How stuff works

Everything will be handled through HTTP requests. No streaming or anything, just basic web stuff.

The API is described more thoroughly in `API.md`, but the basic rundown is this:

1. The client (app) walks around while recording accelerometer/gyroscope data and occasionally videos. They client records all of this data and formats it.
2. Once they're done, they send data to the server through a POST request. The server responds to this request with a unique URL that the client can visit after the data's done processing.
3. The server starts processing the data, and once it's done, makes it available at some web URL that the user can now visit.
