import logging

from flask import Flask
from flask_cors import CORS

from .routes.bookmarks import bookmarks_bp
from .routes.feed import feed_bp

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

app.register_blueprint(feed_bp)
app.register_blueprint(bookmarks_bp)


@app.route('/')
def index():
    return 'Biskuvi Bookmark Server (https://biskuvi-app.github.io)'
