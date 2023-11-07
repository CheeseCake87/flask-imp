from flask import Flask

from app.extensions import imp, db


def create_app():
    app = Flask(__name__)
    imp.init_app(app)
    imp.import_app_resources()
    imp.import_blueprints("blueprints")
    imp.import_models("models")

    db.init_app(app)

    with app.app_context():
        print(app.config['SQLALCHEMY_DATABASE_URI'])
        print(app.config['SQLALCHEMY_BINDS'])
        db.create_all()

    return app
