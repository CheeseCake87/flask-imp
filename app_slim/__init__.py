from flask import Flask

from app_slim.extensions import imp
from flask_imp.config import ImpConfig, FlaskConfig


def create_app():
    app = Flask(__name__, static_url_path="/")

    FlaskConfig(
        secret_key="secret_key",
        app_instance=app
    )

    imp.init_app(app, ImpConfig())
    imp.import_app_resources()
    imp.import_blueprint("www")

    return app
