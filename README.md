# Final project server

## Development setup

First, clone the repository with

```
git clone https://github.com/womogenes/meta-tour.git
```

The code relies on Hector's repository for image stitching, so make sure you have access to [their repository](https://github.com/hectorastrom/Meta-Tour). Then, initialize the submodule with

```
git submodule update --init
```

The server requires Python 3.9 (3.10 breaks everything for some reason), along with the following libraries:

- [Flask](https://flask.palletsprojects.com/en/2.1.x/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/intro.html)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [eventlet](https://eventlet.net/)

All of these are included in `requirements.txt`, so to install all dependencies simply do

```
pip install -r requirements.txt
```

**Important:** for development, setting up a `.env` file containing environment variables in the root directory of the project will be necessary. It needs to contain two keys:

```
MONGO_URL=mongodb+srv://<user>:<password>@.../?retryWrites=true&w=majority
IMGBB_KEY=c3d3...
```

For security, the specific contents of the file aren't tracked in git. Ask William for the exact file!

To start the server, run `python __main__.py`.

### Production

The production server is live at https://meta-tour.herokuapp.com.

## How stuff works

Everything will be handled through HTTP requests. No streaming or anything, just basic web stuff.

The API is described more thoroughly in `API.md`, but the basic rundown is this:

1. The client (app) walks around while recording accelerometer/gyroscope data and occasionally videos. They client records all of this data and formats it.
2. Once they're done, they send data to the server through a POST request. The server redirects the client to a unique URL that the client can visit after the data's done processing.
3. The server starts processing the data, and once it's done, makes it available at the earlier URL, which the user can now visit.
