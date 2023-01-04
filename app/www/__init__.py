from flask_bigapp import Blueprint

bp = Blueprint(__name__)

bp.import_routes("routes")


@bp.before_app_request
def before_app_request():
    bp.init_session()

