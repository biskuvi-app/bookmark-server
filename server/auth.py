from atproto import (
    DidInMemoryCache,
    IdResolver,
    parse_jwt,
    decode_jwt_payload,
    validate_jwt_payload
)
from atproto.exceptions import TokenInvalidSignatureError
from flask import Request


class AuthorizationError(Exception):
    pass


class TokenDecodeError(Exception):
    pass


class AuthService:

    def __init__(self):
        self._cache = DidInMemoryCache()
        self._resolver = IdResolver(cache=self._cache).did.resolve_atproto_key

    @staticmethod
    def validate_auth(request: Request) -> str:
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise AuthorizationError('Authorization header is missing')

        if not auth_header.startswith('Bearer '):
            raise AuthorizationError('Invalid authorization header')

        jwt = auth_header[len('Bearer '):].strip()

        try:
            plain_payload, signing_input, *_, signature = parse_jwt(jwt)
            payload = decode_jwt_payload(plain_payload)
            validate_jwt_payload(payload)

            if payload.iss is None:
                raise TokenDecodeError('Invalid payload. Expected non-None iss')

            return payload.iss

        except TokenInvalidSignatureError as e:
            raise AuthorizationError('Invalid signature') from e


auth_service = AuthService()
