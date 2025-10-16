from flask import Flask

from flask_imp.config import (
    FlaskConfig,
    ImpConfig,
    DatabaseConfig,
    SQLiteDatabaseConfig,
)
from .extensions import db
from .extensions import imp


def create_app():
    app = Flask(
        __name__,
        static_url_path="/static",
        static_folder="static",
        template_folder="templates",
    )
    FlaskConfig(
        secret_key="0000",
    ).apply_config(app)

    app.config["TEST"] = "Hello, World!"

    imp.init_app(
        app,
        ImpConfig(
            init_session={"logged_in": False},
            database_main=SQLiteDatabaseConfig(
                database_name="my_database",
            ),
            database_binds=[
                DatabaseConfig(
                    dialect="sqlite",
                    database_name="database_another",
                    bind_key="another",
                )
            ],
        ),
    )

    imp.import_resources(factories=["collection"])
    imp.import_blueprint("root_blueprint")
    imp.import_blueprints("blueprints")
    imp.import_models("models")

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
