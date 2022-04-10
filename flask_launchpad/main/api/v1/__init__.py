from ...builtins.functions.import_mgr import load_config
from ...builtins.functions.import_mgr import import_routes
from importlib import import_module
from flask import Blueprint
from flask import current_app
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from os import path

config = load_config(from_file_dir=path.dirname(path.realpath(__file__)))
bp = Blueprint(
    name=f"api_{config['settings']['name']}",
    import_name=config['settings']['import_name'],
    url_prefix=f"/api/{config['settings']['name']}"
)
api = Api(app=bp, doc="/docs")
db = SQLAlchemy()
sql_do = db.session


for route in import_routes(module_folder="api", module=config["settings"]["import_name"]):
    import_module(f"{current_app.config['APP_NAME']}.api.{config['settings']['import_name']}.routes.{route}")
