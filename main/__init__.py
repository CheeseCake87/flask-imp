from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ._flask_launchpad.src.flask_launchpad import FlaskLaunchpad
from ._flask_launchpad.src.flask_launchpad import FLStructure

fl = FlaskLaunchpad()
structure = FLStructure()
db = SQLAlchemy()


def create_app():
    main = Flask(__name__)
    fl.init_app(main)
    fl.app_config("app_config.toml")

    structure.init_app(main)
    structure.register_structure("fl_default")

    fl.models_folder("models")
    db.init_app(main)

    fl.import_builtins("flask/routes")
    fl.import_builtins("flask/template_filters")

    fl.import_apis("api")
    fl.import_blueprints("blueprints")

    return main
