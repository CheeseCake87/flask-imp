from ..._flask_bigapp.src.flask_bigapp import BABlueprint

bp = BABlueprint()

bp.import_routes()


@bp.before_app_first_request
def before_app_first_request():
    pass


@bp.before_app_request
def before_app_request():
    bp.init_session()


@bp.after_app_request
def after_app_request(response):
    return response
