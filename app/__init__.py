from flask import Flask

from app.extensions import imp, db


def create_app():
    app = Flask(__name__, static_url_path="/")
    imp.init_app(app, "default.config.toml")
    imp.import_app_resources(
        files_to_import=["*"],
        folders_to_import=["*"],
        factories=["factory_in_folder"]
    )
    imp.import_blueprints("blueprints")
    imp.import_models("models")
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
