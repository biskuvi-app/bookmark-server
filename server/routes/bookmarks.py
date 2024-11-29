from flask import Blueprint, jsonify, request

from ..database import bookmark_manager, BookmarkError
from ..util import get_did, get_uri

bookmarks_bp = Blueprint('bookmarks', __name__)


@bookmarks_bp.route('/xrpc/app.biskuvi.bookmark.isBookmarked', methods=['GET'])
def is_bookmarked():
    value, code = get_did(request)
    if code != 200:
        return value, code
    did = value

    uri = get_uri(request)
    if uri is None:
        return "Bad Request", 400

    try:
        is_bmed = bookmark_manager.is_bookmarked(did, uri)
        return jsonify({"is_bookmarked": is_bmed})
    except BookmarkError:
        return 'Bookmark error', 500


@bookmarks_bp.route('/xrpc/app.biskuvi.bookmark.arePostsBookmarked', methods=['POST'])
def is_bookmarked():
    value, code = get_did(request)
    if code != 200:
        return value, code
    did = value

    json = request.get_json()
    uris: list[str] = json["uris"]
    if uris is None or len(uris) < 1:
        return "Bad Request", 400

    try:
        bookmarked_uris = bookmark_manager.are_posts_bookmarked(did, uris)
        return jsonify({"uris": bookmarked_uris})
    except BookmarkError:
        return 'Bookmark error', 500


@bookmarks_bp.route('/xrpc/app.biskuvi.bookmark.addBookmark', methods=['GET'])
def add_bookmark():
    value, code = get_did(request)
    if code != 200:
        return value, code
    did = value

    uri = get_uri(request)
    if uri is None:
        return "Bad Request", 400

    try:
        bookmark_manager.add_bookmark(did, uri)
        return "", 200
    except BookmarkError:
        return 'Bookmark error', 500


@bookmarks_bp.route('/xrpc/app.biskuvi.bookmark.removeBookmark', methods=['GET'])
def remove_bookmark():
    value, code = get_did(request)
    if code != 200:
        return value, code
    did = value

    uri = get_uri(request)
    if uri is None:
        return "Bad Request", 400

    try:
        bookmark_manager.remove_bookmark(did, uri)
        return "", 200
    except BookmarkError:
        return 'Bookmark error', 500
