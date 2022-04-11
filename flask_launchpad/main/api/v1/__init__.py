from ...builtins.functions.import_mgr import load_config
from ...builtins.functions.import_mgr import import_routes
from importlib import import_module
from flask import Blueprint
from flask import current_app
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from os import path

# Load the config for this API
config = load_config(from_file_dir=path.dirname(path.realpath(__file__)))

# Create a Flask blueprint for this api
bp = Blueprint(
    name=f"api_{config['settings']['name']}",
    import_name=config['settings']['import_name'],
    url_prefix=f"/api/{config['settings']['name']}"
)

# Set the docs URL for this api
api = Api(app=bp, doc=f"api_{config['settings']['name']}/docs")

# Load the SQL controller
db = SQLAlchemy()
sql_do = db.session

# init a dict variable to get external model attributes
extattr = {}

# Pull api enabled blueprints models from the current app config, import and store in dict
for ext_bp, model in current_app.config["API_MODELS"].items():
    extattr[ext_bp] = import_module(f"{current_app.config['APP_NAME']}.blueprints.{ext_bp}.models")

# Import the routes from the route folder
for route in import_routes(module_folder="api", module=config["settings"]["import_name"]):
    import_module(f"{current_app.config['APP_NAME']}.api.{config['settings']['import_name']}.routes.{route}")
