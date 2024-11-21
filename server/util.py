from atproto.exceptions import TokenExpiredSignatureError
from flask import request

from .auth import auth_service, AuthorizationError


def get_uri(req: type(request)) -> (str, int):
    return req.args.get('uri', default=None, type=str)


def get_did(req: type(request)) -> (str, int):
    try:
        return auth_service.validate_auth(req), 200
    except TokenExpiredSignatureError:
        return 'Token expired', 401
    except AuthorizationError as e:
        return str(e), 401
