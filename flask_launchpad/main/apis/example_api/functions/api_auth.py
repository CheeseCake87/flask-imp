from .. import config


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


def public_key_correct(public_api_key: str) -> bool:
    type(config["api"]['public_key'])
    if public_api_key == config["api"]['public_key']:
        return True
    return False
