from importlib import import_module
from flask import Blueprint
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from os import path

from ...builtins.functions.import_mgr import read_config
from ...builtins.functions.import_mgr import import_routes
from ...builtins.functions.structure import StructureBuilder
from ...builtins.functions.database import find_model_location

root = path.dirname(path.realpath(__file__))
config = read_config(filepath=root)
bp = Blueprint(**config["settings"], root_path=root)
struc = StructureBuilder(current_app.config["STRUCTURE"])

db = SQLAlchemy()
sql_do = db.session

account_model = import_module(find_model_location("account"))
FlUser = getattr(account_model, "FlUser")

administrator_model = import_module(find_model_location("administrator"))
FlPermission = getattr(administrator_model, "FlPermission")
FlPermissionMembership = getattr(administrator_model, "FlPermissionMembership")
FlCompany = getattr(administrator_model, "FlCompany")
FlCompanyMembership = getattr(administrator_model, "FlCompanyMembership")
FlTeam = getattr(administrator_model, "FlTeam")
FlTeamMembership = getattr(administrator_model, "FlTeamMembership")

for route in import_routes(module_folder="extensions", module=config["settings"]["name"]):
    import_module(f"{current_app.config['APP_NAME']}.extensions.{config['settings']['name']}.routes.{route}")
