from flask import Blueprint, jsonify

from ..config import Config

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
