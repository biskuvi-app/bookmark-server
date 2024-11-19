from atproto import DidInMemoryCache, IdResolver, parse_jwt, decode_jwt_payload, validate_jwt_payload
from atproto.exceptions import TokenInvalidSignatureError
from flask import Request

_CACHE = DidInMemoryCache()
_ID_RESOLVER = IdResolver(cache=_CACHE).did.resolve_atproto_key


class AuthorizationError(Exception):
    ...


class TokenDecodeError(Exception):
    ...


def validate_auth(request: 'Request') -> str:
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise AuthorizationError('Authorization header is missing')

    if not auth_header.startswith('Bearer '):
        raise AuthorizationError('Invalid authorization header')

    jwt = auth_header[len('Bearer '):].strip()

    try:
        plain_payload, signing_input, _, signature = parse_jwt(jwt)

        payload = decode_jwt_payload(plain_payload)
        validate_jwt_payload(payload)

        if payload.iss is None:
            raise TokenDecodeError('Invalid payload. Expected not None iss')

        return payload.iss

    except TokenInvalidSignatureError as e:
        raise AuthorizationError('Invalid signature') from e
