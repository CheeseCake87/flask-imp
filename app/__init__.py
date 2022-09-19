from flask import Flask
from flask_bigapp import BigApp

bigapp = BigApp()


def create_app():
    main = Flask(__name__)
    bigapp.init_app(main)
    bigapp.import_structures("structures")
    bigapp.import_models(folder="models")
    bigapp.create_all_models()
    bigapp.import_builtins("flask/routes")
    bigapp.import_builtins("flask/template_filters")
    bigapp.import_blueprints("blueprints")
    return main
