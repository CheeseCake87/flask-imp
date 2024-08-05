from flask import Flask

from app_full.extensions import imp, db
from flask_imp.config import ImpConfig, FlaskConfig, DatabaseConfig


def create_app():
    app = Flask(__name__, static_url_path="/")

    FlaskConfig(
        secret_key="secret_key",
        app_instance=app
    )

    imp.init_app(app, ImpConfig(
        init_session={"logged_in": False},
        database_main=DatabaseConfig(
            enabled=True,
            dialect="sqlite"
        )
    ))

    imp.import_app_resources()
    imp.import_blueprint("www")

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
