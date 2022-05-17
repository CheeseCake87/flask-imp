from flask_sqlalchemy import SQLAlchemy
from flask import session

from ...builtins.functions.structure import StructureBuilder
from ..._flask_launchpad.src.flask_launchpad import FLBlueprint

db = SQLAlchemy()
sql_do = db.session

fl_bp = FLBlueprint()
bp = fl_bp.register()
struc = StructureBuilder(fl_bp.config["settings"]["structure"])
fl_bp.import_routes("routes")


@bp.before_app_first_request
def before_app_first_request():
    session.update(fl_bp.session)


@bp.before_app_request
def before_app_request():
    pass


@bp.after_app_request
def after_app_request(response):
    return response
