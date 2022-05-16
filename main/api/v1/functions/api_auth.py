from flask_restx import abort

from .. import fl_bl
config = fl_bl.config()

def check_http_auth(request_authorization) -> bool:
    if request_authorization is None:
        return False
    if "username" not in request_authorization:
        return False
    if "password" not in request_authorization:
        return False
    if request_authorization['username'] != config["api"]['http_user']:
        return False
    if request_authorization['password'] != config["api"]['http_pass']:
        return False
    return True


def public_key_required(pk: str) -> None:
    if not pk == config["public_key"]['public_key']:
        return abort(404)
