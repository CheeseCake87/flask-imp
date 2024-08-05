from flask import Flask

from flask_imp import Imp
from flask_imp.config import ImpConfig, FlaskConfig


def create_app():
    app = Flask(__name__, static_url_path="/")

    FlaskConfig(
        secret_key="secret_key",
        app_instance=app
    )

    imp = Imp(app, ImpConfig())
    imp.import_app_resources()

    return app
