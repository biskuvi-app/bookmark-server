from flask import Blueprint, jsonify

import config

well_known_bp = Blueprint('well-known', __name__)


@well_known_bp.route('/.well-known/atproto-did', methods=['GET'])
def atproto_did():
    return config.SERVICE_DID


@well_known_bp.route('/.well-known/did.json', methods=['GET'])
def did_json():
    return jsonify({
        '@context': ['https://www.w3.org/ns/did/v1'],
        'id': config.SERVICE_DID,
        'service': [
            {
                'id': '#bsky_fg',
                'type': 'BskyFeedGenerator',
                'serviceEndpoint': config.HOSTNAME
            }
        ]
    })
