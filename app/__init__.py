from flask import Flask

from app.config import flask_config, imp_config
from app.extensions import imp, db


def create_app():
    app = Flask(__name__, static_url_path="/")
    flask_config.apply_config(app)

    imp.init_app(app, config=imp_config)
    imp.import_app_resources()
    imp.import_blueprints("blueprints")
    imp.import_models("models")

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
