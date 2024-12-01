from flask import Flask
from flask_cors import CORS

from config import Config
from server.routes.bookmarks import bookmarks_bp
from server.routes.feed import feed_bp
from server.util import get_endpoints

app = Flask(__name__)
CORS(app)

app.register_blueprint(feed_bp)
app.register_blueprint(bookmarks_bp)

xrpc_endpoints = get_endpoints(app)


@app.route('/')
def index():
    return (f'Biskuvi Bookmark Server ({Config.GIT_REPO_URL})<br>'
            f'XRPC endpoints:<br>' +
            "<br>".join(xrpc_endpoints))
