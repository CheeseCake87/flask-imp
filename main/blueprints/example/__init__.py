from ...builtins.functions.structure import StructureBuilder
from flask_sqlalchemy import SQLAlchemy
from ..._flask_launchpad.src.flask_launchpad import FLBlueprint

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

fl_bp = FLBlueprint()
bp = fl_bp.register()
fl_bp.import_routes("routes")

struc = StructureBuilder()
db = SQLAlchemy()
sql_do = db.session
