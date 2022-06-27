from flask import session

from ..._flask_launchpad.src.flask_launchpad import FLBlueprint

fl_bp = FLBlueprint()
bp = fl_bp.register()

# Set the default structure theme for this blueprint ( this can be done route by route also )
stru = "fl_default"

fl_bp.import_routes("routes")


@bp.before_app_first_request
def before_app_first_request():
    pass


@bp.before_app_request
def before_app_request():
    for key in fl_bp.session:
        if key not in session:
            session.update(fl_bp.session)
            break


@bp.after_app_request
def after_app_request(response):
    return response
