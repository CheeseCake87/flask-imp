from ...builtins.functions.import_mgr import read_config
from ...builtins.functions.import_mgr import import_routes
from ...builtins.functions.database import find_model_location
from importlib import import_module
from flask import Blueprint
from flask import current_app
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from os import path

# Load the config for this API
config = read_config(filepath=path.dirname(path.realpath(__file__)))

# Create a Flask blueprint for this api
bp = Blueprint(
    name=f"api_{config['settings']['name']}",
    import_name=config['settings']['import_name'],
    url_prefix=f"/api/{config['settings']['url_prefix']}"
)

# Set the docs URL for this api
api = Api(app=bp, doc=f"api_{config['settings']['name']}/docs")

# Load the SQL controller
db = SQLAlchemy()
sql_do = db.session

api_v1_model = import_module(find_model_location("api_v1"))
ApiExmaple = getattr(api_v1_model, "ApiExmaple")

# Import the routes from the route folder
for route in import_routes(module_folder="api", module=config["settings"]["import_name"]):
    import_module(f"{current_app.config['APP_NAME']}.api.{config['settings']['import_name']}.routes.{route}")
