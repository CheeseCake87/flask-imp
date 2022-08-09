from flask import session

from ..._flask_bigapp.src.flask_bigapp import BABlueprint

ba_bp = BABlueprint()
bp = ba_bp.register()

# Set the default structure theme for this blueprint ( this can be done route by route also )
stru = "fl_default"

ba_bp.import_routes("routes")


@bp.before_app_first_request
def before_app_first_request():
    pass


@bp.before_app_request
def before_app_request():
    for key in ba_bp.session:
        if key not in session:
            session.update(ba_bp.session)
            break


@bp.after_app_request
def after_app_request(response):
    return response
