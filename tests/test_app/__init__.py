import os

from flask import Flask

from flask_imp.auth import encrypt_password, authenticate_password
from flask_imp.config import (
    FlaskConfig,
    ImpConfig,
    DatabaseConfig,
    SQLiteDatabaseConfig,
)
from .extensions import db
from .extensions import imp

os.environ["CONFIG_SECRET_KEY"] = "inserted_from_environment"
os.environ["DB_USERNAME"] = "database_username"
os.environ["DATABASE_NAME"] = "my_database"


def create_app():
    app = Flask(__name__)
    FlaskConfig(
        secret_key=os.getenv("CONFIG_SECRET_KEY"),
    ).apply_config(app)

    app.config["TEST"] = "Hello, World!"

    imp.init_app(
        app,
        ImpConfig(
            init_session={"logged_in": False},
            database_main=SQLiteDatabaseConfig(
                name=os.getenv("DATABASE_NAME", "my_database"),
            ),
            database_binds=[
                DatabaseConfig(
                    dialect="sqlite",
                    name="database_another",
                    bind_key="another",
                )
            ],
        ),
    )

    imp.import_app_resources(factories=["collection"])
    imp.import_blueprint("root_blueprint")
    imp.import_blueprints("blueprints")
    imp.import_models("models")

    db.init_app(app)

    for key, value in app.config.items():
        print(f"{key}: {value}")

    with app.app_context():
        db.create_all()

    print(app.config["TEST"])

    password = "password"

    encrypted_password = encrypt_password(password, "salt", 512, 1, "start")

    print(encrypted_password)

    print(authenticate_password(password, encrypted_password, "salt", 512, 1, "start"))

    return app
