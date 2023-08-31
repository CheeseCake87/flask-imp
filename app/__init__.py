import os

from flask import Flask
from app.extensions import bigapp
from app.extensions import db

os.environ["CONFIG_SECRET_KEY"] = "inserted_from_environment"
os.environ["DB_USERNAME"] = "database_username"


def create_app():
    app = Flask(__name__)
    bigapp.init_app(app, ignore_missing_env_variables=True)
    db.init_app(app)

    bigapp.import_app_resources(
        app_factories=["collection"],
        scope_root_files_to=["root_routes.py"]
    )

    bigapp.import_blueprint("root_blueprint")
    bigapp.import_blueprints("blueprints")

    bigapp.import_models("models")

    with app.app_context():
        db.create_all()

    return app
