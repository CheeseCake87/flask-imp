from flask import session
from flask import url_for

from ..._flask_bigapp.src.flask_bigapp import Blueprint

bp = Blueprint(__name__)

# Set the default structure theme for this blueprint ( this can be done route by route also )
stru = "bigapp_default"

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
