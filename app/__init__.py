import os

from flask import Flask

from app.extensions import db
from app.extensions import imp
from flask_imp.auth import encrypt_password, authenticate_password

os.environ["CONFIG_SECRET_KEY"] = "inserted_from_environment"
os.environ["DB_USERNAME"] = "database_username"


def create_app():
    app = Flask(__name__)
    imp.init_app(app, ignore_missing_env_variables=True)
    db.init_app(app)

    imp.import_app_resources(
        app_factories=["collection"]
    )

    print(app.config["TEST"])

    imp.import_blueprint("root_blueprint")
    imp.import_blueprints("blueprints")

    imp.import_models("models")

    with app.app_context():
        db.create_all()

    password = "password"

    encrypted_password = encrypt_password(
        password, "salt", 512, 1, "start"
    )

    print(encrypted_password)

    print(
        authenticate_password(
            password, encrypted_password, "salt", 512, 1, "start"
        )
    )

    return app
