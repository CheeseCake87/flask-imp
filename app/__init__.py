import logging

from flask import Flask

from app.extensions import imp, db
from flask_imp.config import DatabaseConfig
from flask_imp.config import FlaskConfig
from flask_imp.config import ImpConfig

logging.basicConfig(level=logging.DEBUG)

flask_config = FlaskConfig(
    debug=True,
    secret_key="secret_key",
)

imp_config = ImpConfig(
    init_session={
        "logged_in": False,
    },
    database_main=DatabaseConfig(
        enabled=True,
        dialect="sqlite",
    )
)


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
