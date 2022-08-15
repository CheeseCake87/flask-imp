from flask import session

from ..._flask_bigapp.src.flask_bigapp import BABlueprint

bp = BABlueprint()

# Set the default structure theme for this blueprint ( this can be done route by route also )
stru = "fl_default"

bp.import_routes("routes")


@bp.before_app_first_request
def before_app_first_request():
    pass


@bp.before_app_request
def before_app_request():
    bp.init_session()


@bp.after_app_request
def after_app_request(response):
    return response
