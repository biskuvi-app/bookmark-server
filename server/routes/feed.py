from flask import Blueprint, jsonify, request

from ..auth import auth_service, AuthorizationError
from ..config import Config
from ..database import bookmark_manager, EMPTY_FEED
from ..logger import logger

feed_bp = Blueprint('feed', __name__)


@feed_bp.route('/.well-known/did.json', methods=['GET'])
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
    try:
        did = auth_service.validate_auth(request)
    except AuthorizationError as e:
        logger.error(e)
        return jsonify(EMPTY_FEED)

    try:
        cursor = request.args.get('cursor', default=None, type=str)
        limit = request.args.get('limit', default=20, type=int)
    except ValueError as e:
        logger.error(e)
        return 'Malformed cursor', 400

    return jsonify(bookmark_manager.get_bookmarks(did, cursor, limit))
