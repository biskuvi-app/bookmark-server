import logging

from flask import Blueprint, jsonify, request

from ..auth import auth_service, AuthorizationError
from ..database import bookmark_manager, BookmarkError

bookmarks_bp = Blueprint('bookmarks', __name__)


@bookmarks_bp.route('/xrpc/app.bsky.feed.getFeedSkeleton', methods=['GET'])
def get_feed_skeleton():
    try:
        did = auth_service.validate_auth(request)
    except AuthorizationError as e:
        logging.error(e)
        return 'Unauthorized', 401

    try:
        cursor = request.args.get('cursor', default=None, type=str)
        limit = request.args.get('limit', default=20, type=int)
    except ValueError:
        return 'Malformed cursor', 400

    return jsonify(bookmark_manager.get_bookmarks(did, cursor, limit))


@bookmarks_bp.route('/xrpc/app.biskuvi.bookmark.isBookmarked', methods=['GET'])
def is_bookmarked():
    try:
        did = auth_service.validate_auth(request)
    except AuthorizationError:
        return 'Unauthorized', 401

    uri = request.args.get('uri', default=None, type=str)
    if uri is None:
        return "Bad Request", 400

    try:
        is_bmed = bookmark_manager.is_bookmarked(did, uri)
        return jsonify({'success': True, "is_bookmarked": is_bmed})
    except BookmarkError:
        return 'Bookmark error', 500


@bookmarks_bp.route('/xrpc/app.biskuvi.bookmark.addBookmark', methods=['GET'])
def add_bookmark():
    try:
        did = auth_service.validate_auth(request)
    except AuthorizationError:
        return 'Unauthorized', 401

    uri = request.args.get('uri', default=None, type=str)
    if uri is None:
        return "Bad Request", 400

    try:
        bookmark_manager.add_bookmark(did, uri)
        return jsonify({'success': True})
    except BookmarkError:
        return 'Bookmark error', 500


@bookmarks_bp.route('/xrpc/app.biskuvi.bookmark.removeBookmark', methods=['GET'])
def remove_bookmark():
    try:
        did = auth_service.validate_auth(request)
    except AuthorizationError:
        return 'Unauthorized', 401

    uri = request.args.get('uri', default=None, type=str)
    if uri is None:
        return "Bad Request", 400

    try:
        bookmark_manager.remove_bookmark(did, uri)
        return jsonify({'success': True})
    except BookmarkError:
        return 'Bookmark error', 500
