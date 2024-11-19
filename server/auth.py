import logging

import atproto
from atproto import DidInMemoryCache, IdResolver, verify_jwt
from atproto.exceptions import TokenInvalidSignatureError
from flask import Request

_CACHE = DidInMemoryCache()
_ID_RESOLVER = IdResolver(cache=_CACHE)


class AuthorizationError(Exception):
    ...


def validate_auth(request: 'Request') -> str:
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise AuthorizationError('Authorization header is missing')

    if not auth_header.startswith('Bearer '):
        raise AuthorizationError('Invalid authorization header')

    jwt = auth_header[len('Bearer '):].strip()

    try:
        # return verify_jwt(jwt, _ID_RESOLVER.did.resolve_atproto_key).iss
        payload = atproto.decode_jwt_payload(jwt)
        did = payload.iss
        logging.info(did)
        return did
    except TokenInvalidSignatureError as e:
        raise AuthorizationError('Invalid signature') from e
