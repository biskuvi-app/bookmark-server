from atproto import (
    DidInMemoryCache,
    IdResolver
)
from atproto_server.auth.jwt import verify_jwt
from flask import Request


class AuthorizationError(Exception):
    pass


class AuthService:
    _cache = DidInMemoryCache()
    _resolver = IdResolver(cache=_cache).did.resolve_atproto_key

    def validate_auth(self, request: Request) -> str:
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise AuthorizationError('Authorization header is missing')

        auth_header_split = auth_header.split(" ", 1)

        if len(auth_header_split) != 2:
            raise AuthorizationError('Invalid Authorization header content')

        prefix = auth_header_split[0]
        jwt = auth_header_split[1].strip()
        match prefix:
            case 'Bearer':
                return verify_jwt(jwt, self._resolver).iss
            case 'DPoP':
                return verify_jwt(jwt, self._resolver).sub
            case _:
                raise AuthorizationError(f'Unsupported Authorization header prefix: {prefix}')


auth_service = AuthService()
