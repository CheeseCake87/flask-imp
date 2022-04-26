from ....builtins.functions.utilities import set_session_init

from .. import bp
from .. import config


@bp.before_app_first_request
def before_app_first_request():
    pass


@bp.before_app_request
def before_app_request():
    set_session_init(config)


@bp.after_app_request
def after_app_request(response):
    return response
