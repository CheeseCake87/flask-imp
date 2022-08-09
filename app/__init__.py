from flask import Flask
from ._flask_bigapp.src.flask_bigapp import BApp
from ._flask_bigapp.src.flask_bigapp import BAStructure
from ._flask_bigapp.src.flask_bigapp import Security

bapp = BApp()
structures = BAStructure()
security = Security()


def create_app():
    main = Flask(__name__)
    bapp.init_app(main)
    bapp.app_config("app_config.toml")

    security.init_app(main)

    bapp.models(folder="models")

    structures.init_app(main, "structures")
    structures.register_structure("fl_default")

    bapp.import_builtins("flask/routes")
    bapp.import_builtins("flask/template_filters")

    bapp.import_apis("api")
    bapp.import_blueprints("blueprints")

    return main
