from importlib import import_module
from flask_sqlalchemy import SQLAlchemy
from flask import session

from ...builtins.functions.database import find_model_location
from ...builtins.functions.structure import StructureBuilder
from ..._flask_launchpad.src.flask_launchpad import FLBlueprint

db = SQLAlchemy()
sql_do = db.session

account_model = import_module(find_model_location("account"))
FlUser = getattr(account_model, "FlUser")

administrator_model = import_module(find_model_location("administrator"))
FlPermission = getattr(administrator_model, "FlPermission")
FlPermissionMembership = getattr(administrator_model, "FlPermissionMembership")

system_model = import_module(find_model_location("system"))
FlSystemSettings = getattr(system_model, "FlSystemSettings")

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
