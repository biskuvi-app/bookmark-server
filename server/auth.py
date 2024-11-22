from atproto import (
    DidInMemoryCache,
    IdResolver
)
from atproto_server.auth.jwt import verify_jwt, parse_jwt, decode_jwt_payload, validate_jwt_payload
from flask import Request


class AuthorizationError(Exception):
    pass


class AuthService:
    _cache = DidInMemoryCache()
    _resolver = IdResolver(cache=_cache).did.resolve_atproto_key

    @staticmethod
    def validate_auth(request: Request) -> str:
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise AuthorizationError('Authorization header is missing')

        auth_header_split = auth_header.split(" ", 1)

        if len(auth_header_split) != 2:
            raise AuthorizationError('Invalid Authorization header content')

        prefix = auth_header_split[0]
        jwt = auth_header_split[1].strip()
        match prefix:
            case 'Bearer' | 'DPoP':
                # payload = verify_jwt(jwt, self._resolver).iss

                # temporary workaround due to error when using verify_jwt

                plain_payload, signing_input, *_, signature = parse_jwt(jwt)
                payload = decode_jwt_payload(plain_payload)
                validate_jwt_payload(payload)
                match prefix:
                    case 'Bearer':
                        return payload.iss
                    case 'DPoP':
                        return payload.sub
            case _:
                raise AuthorizationError(f'Unsupported Authorization header prefix: {prefix}')


auth_service = AuthService()
