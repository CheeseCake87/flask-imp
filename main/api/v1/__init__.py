from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask import session

from ..._flask_launchpad.src.flask_launchpad import FLBlueprint

fl_bl = FLBlueprint()

api_bp = fl_bl.register()
api = Api(api_bp, doc=f"/docs")

fl_bl.import_routes()

db = SQLAlchemy()
sql_do = db.session


@api_bp.before_app_first_request
def before_app_first_request():
    session.update(fl_bl.session)


@api_bp.before_app_request
def before_app_request():
    pass


@api_bp.after_app_request
def after_app_request(response):
    return response
