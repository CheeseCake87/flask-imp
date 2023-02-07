import os
import secrets

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_bigapp import BigApp

bigapp = BigApp()
db = SQLAlchemy()

os.environ["CONFIG_SECRET_KEY"] = secrets.token_urlsafe(128)


def create_app():
    app = Flask(__name__)
    bigapp.init_app(app)
    db.init_app(app)

    bigapp.import_builtins()
    bigapp.import_blueprint("www")
    bigapp.import_blueprint("tests")
    bigapp.import_theme("theme")

    bigapp.import_models(from_folder="models")

    @app.before_request
    def before_request():
        bigapp.init_session()

    return app
