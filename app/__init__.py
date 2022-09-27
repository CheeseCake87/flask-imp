from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_bigapp import BigApp

bigapp = BigApp()
db = SQLAlchemy()


def create_app():
    main = Flask(__name__)
    bigapp.init_app(main, db)
    bigapp.import_structures("structures")
    bigapp.import_models(folder="models")
    bigapp.import_builtins("flask/routes")
    bigapp.import_builtins("flask/template_filters")
    bigapp.import_blueprints("blueprints")

    with main.app_context():
        bigapp.db.create_all()

    # for _ in main.url_map.iter_rules():
    #     print(_)
    return main
