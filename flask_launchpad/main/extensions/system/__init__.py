from ...builtins.functions.import_mgr import read_config
from ...builtins.functions.import_mgr import import_routes
from ...builtins.functions.structure import StructureBuilder
from importlib import import_module
from flask import Blueprint
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import engine
from os import path

"""
This is an example blueprint init file.
1. Config file is loaded into a dict and the arguments are passed direct to the blueprint object
2. Root path is set to allow the static url path to work
3. SQLAlchemy object is created
4. database session is set to sql_do to make it easier to read and use in sql action files
5. init a dict variable to get external model attributes
6. Pull blueprint models from the current app config, import and store in dict
. routes in the routes folder of the blueprint are imported
"""

config = read_config(from_file_dir=path.dirname(path.realpath(__file__)))
bp = Blueprint(**config["settings"], root_path=path.dirname(path.realpath(__file__)))

db = SQLAlchemy()
sql_do = db.session
sql_test = engine.Engine

struc = StructureBuilder(current_app.config["STRUCTURE"])

for route in import_routes(module_folder="extensions", module=config["settings"]["name"]):
    import_module(f"{current_app.config['APP_NAME']}.extensions.{config['settings']['name']}.routes.{route}")
