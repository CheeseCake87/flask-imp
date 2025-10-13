def init_full_py(app_name: str, secret_key: str) -> str:
    return f"""\
from flask import Flask

from {app_name}.extensions import imp, db
from flask_imp.config import ImpConfig, FlaskConfig, DatabaseConfig


def create_app():
    app = Flask(
        __name__,
        static_url_path="/",
        static_folder="static",
        template_folder="templates",
    )

    FlaskConfig(
        secret_key="{secret_key}",
        app_instance=app
    )

    imp.init_app(app, ImpConfig(
        init_session={{"logged_in": False}},
        database_main=DatabaseConfig(
            enabled=True,
            dialect="sqlite"
        )
    ))

    imp.import_resources()
    imp.import_blueprints("blueprints")
    imp.import_models("models")

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
"""


def init_slim_py(app_name: str, secret_key: str) -> str:
    return f"""\
from flask import Flask

from {app_name}.extensions import imp
from flask_imp.config import ImpConfig, FlaskConfig


def create_app():
    app = Flask(
        __name__,
        static_url_path="/",
        static_folder="static",
        template_folder="templates",
    )

    FlaskConfig(
        secret_key="{secret_key}",
        app_instance=app
    )

    imp.init_app(app, ImpConfig())
    imp.import_resources()
    imp.import_blueprint("www")

    return app
"""


def init_minimal_py(secret_key: str) -> str:
    return f"""\
from flask import Flask

from flask_imp import Imp
from flask_imp.config import ImpConfig, FlaskConfig


def create_app():
    app = Flask(
        __name__,
        static_url_path="/",
        static_folder="static",
        template_folder="templates",
    )

    FlaskConfig(
        secret_key="{secret_key}",
        app_instance=app
    )

    imp = Imp(app, ImpConfig())
    imp.import_resources()

    return app
"""
