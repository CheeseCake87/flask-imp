from flask import Flask
from ._flask_bigapp.src.flask_bigapp import BigApp

bigapp = BigApp()


def create_app():
    main = Flask(__name__)
    bigapp.init_app(main, "app_config.toml")

    bigapp.import_models(folder="models")

    bigapp.import_structures("structures")

    bigapp.import_builtins("flask/routes")
    bigapp.import_builtins("flask/template_filters")

    bigapp.import_blueprints("blueprints")

    return main
