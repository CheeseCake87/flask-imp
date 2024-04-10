from flask_imp import Blueprint

bp = Blueprint(__name__, "config.Config")

bp.import_resources("routes")
bp.import_models("models")


@bp.before_app_request
def before_app_request():
    bp.init_session()
