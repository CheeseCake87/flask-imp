from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ._flask_launchpad.src.flask_launchpad import FlaskLaunchpad

fl = FlaskLaunchpad()
db = SQLAlchemy()


def create_app():
    main = Flask(__name__)
    fl.init_app(main)
    fl.app_config("app_config.toml")
    fl.models_folder("models")

    fl.register_structure_folder("structures")

    fl.import_builtins("builtins/routes")
    fl.import_builtins("builtins/template_filters")

    fl.import_apis("api")
    fl.import_blueprints("blueprints")

    return main
