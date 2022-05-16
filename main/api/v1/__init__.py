from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from ..._flask_launchpad.src.flask_launchpad import FLBlueprint

fl_bl = FLBlueprint()
api_bp = fl_bl.register()
api = Api(api_bp, doc=f"/docs")
fl_bl.import_routes()
db = SQLAlchemy()
sql_do = db.session
