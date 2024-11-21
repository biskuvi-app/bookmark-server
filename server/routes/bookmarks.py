from flask import Blueprint, jsonify, request

from ..auth import auth_service, AuthorizationError
from ..database import bookmark_manager, BookmarkError
from ..logger import logger

bookmarks_bp = Blueprint('bookmarks', __name__)


@bookmarks_bp.route('/xrpc/app.biskuvi.bookmark.isBookmarked', methods=['GET'])
def is_bookmarked():
    try:
        did = auth_service.validate_auth(request)
    except AuthorizationError as e:
        logger.error(e)
        return 'Unauthorized', 401

    uri = request.args.get('uri', default=None, type=str)
    if uri is None:
        return "Bad Request", 400

    try:
        is_bmed = bookmark_manager.is_bookmarked(did, uri)
        return jsonify({'success': True, "is_bookmarked": is_bmed})
    except BookmarkError as e:
        logger.error(e)
        return 'Bookmark error', 500


@bookmarks_bp.route('/xrpc/app.biskuvi.bookmark.addBookmark', methods=['GET'])
def add_bookmark():
    try:
        did = auth_service.validate_auth(request)
    except AuthorizationError as e:
        logger.error(e)
        return 'Unauthorized', 401

    uri = request.args.get('uri', default=None, type=str)
    if uri is None:
        return "Bad Request", 400

    try:
        bookmark_manager.add_bookmark(did, uri)
        return jsonify({'success': True})
    except BookmarkError as e:
        logger.error(e)
        return 'Bookmark error', 500


@bookmarks_bp.route('/xrpc/app.biskuvi.bookmark.removeBookmark', methods=['GET'])
def remove_bookmark():
    try:
        did = auth_service.validate_auth(request)
    except AuthorizationError as e:
        logger.error(e)
        return 'Unauthorized', 401

    uri = request.args.get('uri', default=None, type=str)
    if uri is None:
        return "Bad Request", 400

    try:
        bookmark_manager.remove_bookmark(did, uri)
        return jsonify({'success': True})
    except BookmarkError as e:
        logger.error(e)
        return 'Bookmark error', 500
