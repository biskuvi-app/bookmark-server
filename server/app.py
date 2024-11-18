from server.auth import validate_auth, AuthorizationError
from flask import Flask, jsonify, request
from server.database import Databases, BookmarkError


# noinspection SpellCheckingInspection
class Config:
    HOSTNAME = "biskuvibookmark.pythonanywhere.com"
    SERVICE_DID = f"did:plc:qvmvynssslo5yhstrnc2cwv6"
    BOOKMARKS_URI = f"at://{SERVICE_DID}/app.bsky.feed.generator/bookmarks"


app = Flask(__name__)
databases = Databases()


@app.route('/')
def index():
    return 'Biskuvi Bookmark Server (https://biskuvi-app.github.io)'


@app.route('/.well-known/did.json', methods=['GET'])
def did_json():
    return jsonify({
        '@context': ['https://www.w3.org/ns/did/v1'],
        'id': Config.SERVICE_DID,
        'service': [
            {
                'id': '#bsky_fg',
                'type': 'BskyFeedGenerator',
                'serviceEndpoint': f'https://{Config.HOSTNAME}'
            }
        ]
    })


@app.route('/xrpc/app.bsky.feed.describeFeedGenerator', methods=['GET'])
def describe_feed_generator():
    feeds = [{'uri': uri} for uri in {}]
    response = {
        'encoding': 'application/json',
        'body': {
            'did': Config.SERVICE_DID,
            'feeds': feeds
        }
    }
    return jsonify(response)


@app.route('/xrpc/app.bsky.feed.getFeedSkeleton', methods=['GET'])
def get_feed_skeleton():
    feed = request.args.get('feed', default=None, type=str)

    try:
        requester_did = validate_auth(request)
    except AuthorizationError:
        return 'Unauthorized', 401

    try:
        cursor = request.args.get('cursor', default=None, type=str)
        limit = request.args.get('limit', default=20, type=int)
    except ValueError:
        return 'Malformed cursor', 400

    return jsonify({})


@app.route('/xrpc/app.biskuvi.bookmark.isBookmarked', methods=['GET'])
def is_bookmarked():
    uri = request.args.get('uri', default=None, type=str)
    if uri is None:
        return "Bad Request", 400
    try:
        did = validate_auth(request)
        databases.repo_bookmarks(did).is_bookmarked(uri)
    except AuthorizationError:
        return 'Unauthorized', 401
    except BookmarkError:
        return 'Unauthorized', 405

    return jsonify({'success': True, })


@app.route('/xrpc/app.biskuvi.bookmark.addBookmark', methods=['GET'])
def add_bookmark():
    uri = request.args.get('uri', default=None, type=str)
    if uri is None:
        return "Bad Request", 400
    return jsonify({'success': True})


@app.route('/xrpc/app.biskuvi.bookmark.removeBookmark', methods=['GET'])
def remove_bookmark():
    uri = request.args.get('uri', default=None, type=str)
    if uri is None:
        return "Bad Request", 400
    return jsonify({'success': True})
