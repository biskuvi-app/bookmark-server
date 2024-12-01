from atproto.exceptions import TokenExpiredSignatureError
from flask import request, Flask
from werkzeug.routing import Rule

from server.auth import auth_service, AuthorizationError


def get_uri(req: type(request)) -> (str, int):
    return req.args.get('uri', default=None, type=str)


def get_did(req: type(request)) -> (str, int):
    try:
        return auth_service.validate_auth(req), 200
    except TokenExpiredSignatureError:
        return 'Token expired', 401
    except AuthorizationError as e:
        return str(e), 401


def get_endpoints(app: Flask):
    xrpc_endpoints = []

    map_items = app.url_map.__dict__.items()
    for map_key, rules in map_items:
        if map_key == "_rules_by_endpoint":
            for rule_key, rule_list_item in rules.items():
                rule_list: list[Rule] = rule_list_item
                for rule in rule_list:
                    rule: Rule = rule
                    parts = []
                    # noinspection PyProtectedMember
                    for is_dynamic, data in rule._trace:
                        if is_dynamic:
                            parts.append(f"<{data}>")
                        else:
                            parts.append(data)
                    parts_str = "".join(parts).lstrip("|")
                    if parts_str.startswith("/xrpc"):
                        xrpc_endpoints.append(parts_str)

    return xrpc_endpoints
