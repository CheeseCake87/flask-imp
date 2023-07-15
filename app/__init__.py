import os
import secrets

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_bigapp import BigApp

bigapp = BigApp()
db = SQLAlchemy()

os.environ["CONFIG_SECRET_KEY"] = secrets.token_urlsafe(128)
os.environ["DB_USERNAME"] = "database_username"


def create_app():
    app = Flask(__name__)
    bigapp.init_app(app, ignore_missing_env_variables=True)
    db.init_app(app)

    bigapp.import_global_collection()
    # bigapp.import_builtins()
    # bigapp.import_blueprint("www")
    # bigapp.import_blueprint("tests")
    # bigapp.import_blueprints("blueprints")
    # bigapp.import_theme("theme")
    # bigapp.import_models(from_folder="models")

    # with app.app_context():
    #     db.create_all()

    return app
