from flask import Flask
from ._flask_launchpad.src.flask_launchpad import FlaskLaunchpad

fl = FlaskLaunchpad()


def create_app():
    main = Flask(__name__)
    fl.init_app(main)

    fl.app_config("app_config.toml")
    fl.register_structure_folder("structures")
    fl.import_builtins("builtins/routes")
    fl.import_builtins("builtins/template_filters")
    fl.import_blueprints("blueprints")
    fl.import_blueprints("extensions")
    fl.import_apis("api")

    # fl.import_blueprints("extensions")

    # for rule in main.url_map.iter_rules():
    #     print(rule)
    #
    # for key, value in main.config.items():
    #     print(key, value)

    print(main.config)

    return main
