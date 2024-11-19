import logging

from flask_cors import CORS

from server.auth import validate_auth, AuthorizationError
from flask import Flask, jsonify, request
from server.database import Databases, BookmarkError


# noinspection SpellCheckingInspection
class Config:
    HOSTNAME = "biskuvibookmark.pythonanywhere.com"
    SERVICE_DID = f"did:plc:qvmvynssslo5yhstrnc2cwv6"
    BOOKMARKS_URI = f"at://{SERVICE_DID}/app.bsky.feed.generator/bookmarks"


app = Flask(__name__)
CORS(app)
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
    response = {
        'encoding': 'application/json',
        'body': {
            'did': Config.SERVICE_DID,
            'feeds': [{'uri': Config.BOOKMARKS_URI}]
        }
    }
    return jsonify(response)


@app.route('/xrpc/app.bsky.feed.getFeedSkeleton', methods=['GET'])
def get_feed_skeleton():
    did: str
    try:
        did = validate_auth(request)
    except AuthorizationError:
        return 'Unauthorized', 401

    cursor: str
    limit: int
    try:
        cursor = request.args.get('cursor', default=None, type=str)
        limit = request.args.get('limit', default=20, type=int)
    except ValueError:
        return 'Malformed cursor', 400

    return jsonify(databases.get_bookmarks(did, cursor, limit))


@app.route('/xrpc/app.biskuvi.bookmark.isBookmarked', methods=['GET'])
def is_bookmarked():
    did: str
    try:
        did = validate_auth(request)
    except AuthorizationError:
        return 'Unauthorized', 401

    uri = request.args.get('uri', default=None, type=str)
    if uri is None:
        return "Bad Request", 400

    is_bmed: bool
    try:
        is_bmed = databases.is_bookmarked(did, uri)
    except BookmarkError:
        return 'Bookmark error', 500

    return jsonify({'success': True, "is_bookmarked": is_bmed})


@app.route('/xrpc/app.biskuvi.bookmark.addBookmark', methods=['GET'])
def add_bookmark():
    did: str
    try:
        did = validate_auth(request)
    except AuthorizationError:
        return 'Unauthorized', 401

    uri = request.args.get('uri', default=None, type=str)
    if uri is None:
        return "Bad Request", 400

    try:
        databases.add_bookmark(did, uri)
    except BookmarkError:
        return 'Bookmark error', 500

    return jsonify({'success': True})


@app.route('/xrpc/app.biskuvi.bookmark.removeBookmark', methods=['GET'])
def remove_bookmark():
    did: str
    try:
        did = validate_auth(request)
    except AuthorizationError:
        return 'Unauthorized', 401

    uri = request.args.get('uri', default=None, type=str)
    if uri is None:
        return "Bad Request", 400

    try:
        databases.remove_bookmark(did, uri)
    except BookmarkError:
        return 'Bookmark error', 500

    return jsonify({'success': True})
