from flask import Blueprint, jsonify, request

from config import Config
from server.database import bookmark_manager, EMPTY_FEED
from server.util import get_did

feed_bp = Blueprint('feed', __name__)


@feed_bp.route('/.well-known/atproto-did', methods=['GET'])
def atproto_did():
    return jsonify(Config.SERVICE_DID)


@feed_bp.route('/.well-known/did.json', methods=['GET'])
def did_json():
    return jsonify({
        '@context': ['https://www.w3.org/ns/did/v1'],
        'id': f"did:web:{Config.HOSTNAME}",
        'service': [
            {
                'id': '#bsky_fg',
                'type': 'BskyFeedGenerator',
                'serviceEndpoint': f'https://{Config.HOSTNAME}'
            }
        ]
    })


@feed_bp.route('/xrpc/app.bsky.feed.describeFeedGenerator', methods=['GET'])
def describe_feed_generator():
    return jsonify({
        'encoding': 'application/json',
        'body': {
            'did': Config.SERVICE_DID,
            'feeds': [{'uri': Config.BOOKMARKS_URI}]
        }
    })


@feed_bp.route('/xrpc/app.bsky.feed.getFeedSkeleton', methods=['GET'])
def get_feed_skeleton():
    value, code = get_did(request)
    if code != 200:
        return jsonify(EMPTY_FEED), code
    did = value

    try:
        cursor = request.args.get('cursor', default=None, type=str)
        limit = request.args.get('limit', default=50, type=int)
    except ValueError:
        return 'Malformed cursor', 400

    return jsonify(bookmark_manager.get_bookmarks(did, cursor, limit)), 200
