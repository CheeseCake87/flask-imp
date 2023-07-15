from flask_bigapp import Blueprint

bp = Blueprint(__name__)

bp.import_resource("routes")
bp.import_resource("error_handlers")


@bp.before_app_request
def before_app_request():
    bp.init_session()
