from .. import bp


@bp.before_app_request
def before_app_request():
    pass


@bp.after_app_request
def after_app_request(response):
    return response
