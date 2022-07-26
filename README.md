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

## Production

Not entirely figured out yet, but there's currently a Heroku app running this with gunicorn at https://meta-tour.herokuapp.com.

## How stuff works

The server opens a socket.io that has a single event for now called `motion-reading`. Currently it just logs the data, but this will be passed onto our other scripts in the future.

We plan to add a `camera-reading` event that takes in image data too.
