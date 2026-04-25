def init_full_py(app_name: str) -> str:
    return f"""\
from flask import Flask

from {app_name}.extensions import imp, db
from {app_name}.config import FLASK_CONFIG, IMP_CONFIG


def create_app():
    app = Flask(
        __name__,
        static_url_path="/",
        static_folder="static",
        template_folder="templates",
    )
    app.config.from_object(FLASK_CONFIG.as_object())

    imp.init_app(app, IMP_CONFIG)
    imp.import_resources()
    imp.import_blueprints("blueprints")
    imp.import_models("models")

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
"""


def init_slim_py(app_name: str) -> str:
    return f"""\
from flask import Flask

from {app_name}.extensions import imp
from {app_name}.config import FLASK_CONFIG, IMP_CONFIG


def create_app():
    app = Flask(
        __name__,
        static_url_path="/",
        static_folder="static",
        template_folder="templates",
    )
    app.config.from_object(FLASK_CONFIG.as_object())

    imp.init_app(app, IMP_CONFIG)
    imp.import_resources()
    imp.import_blueprint("www")

    return app
"""


def init_minimal_py(app_name: str) -> str:
    return f"""\
from flask import Flask

from {app_name}.extensions import imp
from {app_name}.config import FLASK_CONFIG, IMP_CONFIG


def create_app():
    app = Flask(
        __name__,
        static_url_path="/",
        static_folder="static",
        template_folder="templates",
    )
    app.config.from_object(FLASK_CONFIG.as_object())

    imp.init_app(app, IMP_CONFIG)
    imp.import_resources()

    return app
"""
