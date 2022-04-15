from .builtins.functions.email_connector import test_email_server_connection
from .builtins.functions.email_connector import send_email
from .builtins.functions.import_mgr import show_stats
from .builtins.functions.import_mgr import read_config
from .builtins.functions.import_mgr import load_modules
from .builtins.functions.import_mgr import import_routes
from .builtins.functions.utilities import building_rocket
from .builtins.functions.utilities import rocket_launched
from .builtins.functions.utilities import email_server_status
from importlib import import_module
from datetime import timedelta
from flask import Flask
from os import path

settings = read_config(app_config=True)
app_name = settings["app"]["name"]
app_root = settings["app"]["root"]


class Config(object):
    APP_NAME = app_name
    VERSION = settings["frameworks"]["launchpad"]
    SECRET_KEY = settings["app"]["secret_key"]
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=int(settings["app"]["session_time"]))
    DEBUG = settings["app"]["debug"]
    TESTING = settings["app"]["testing"]
    UPLOAD_FOLDER = f"{app_root}/uploads"
    ERROR_404_HELP = settings["app"]["error_404_help"]
    STRUCTURE = settings["app"]["structure"]
    SHARED_MODELS = {}
    if settings["database"]["enabled"]:
        _db = settings["database"]["name"]
        _u = settings["database"]["username"]
        _p = settings["database"]["password"]
        if settings["database"]["type"] == "sqlite":
            SQLALCHEMY_DATABASE_URI = f"{settings['database']['type']}:///{app_root}/database.db"
        else:
            SQLALCHEMY_DATABASE_URI = f"{settings['database']['type']}://{_u}:{_p}@localhost/{_db}"
        SQLALCHEMY_TRACK_MODIFICATIONS = True


def create_app(live: bool):
    main = Flask(__name__)
    main.config.from_object(Config)
    main.template_folder = settings["app"]["template_folder"]
    main.static_folder = settings["app"]["static_folder"]

    show_stats(building_rocket(), live)
    show_stats(f">> {settings['frameworks']['launchpad']}", live)
    show_stats(email_server_status(settings["smtp"]["enabled"]), live)
    show_stats(f">> {settings['smtp']['server']}, {settings['smtp']['port']}, {settings['smtp']['username']}", live)
    show_stats("!! Got to: http://127.0.0.1:5000/system/test-email to test. !!", live)
    show_stats(" ", live)
    show_stats(f":: GLOBAL JS : {settings['frameworks']['global_js']} ::", live)
    show_stats(f":: GLOBAL CSS : {settings['frameworks']['global_css']} ::", live)

    with main.app_context():
        def load_blueprints() -> None:
            for bp_name in load_modules(module_folder="blueprints"):
                try:
                    blueprint_module = import_module(f"{app_name}.blueprints.{bp_name}")
                    blueprint_object = getattr(blueprint_module, "bp")
                    main.register_blueprint(blueprint_object, name=f"{bp_name}")
                    show_stats(f":+ BLUEPRINT REGISTERED [{bp_name}] +:", live)
                except AttributeError:
                    show_stats(f":! ERROR REGISTERING BLUEPRINT [{bp_name}]: No import attribute found !:")
                    continue

                if path.isfile(f"{app_root}/blueprints/{bp_name}/models.py"):
                    models_module = import_module(f"{app_name}.blueprints.{bp_name}.models")
                    try:
                        import_object = getattr(models_module, "db")
                        import_object.init_app(main)
                        bp_config = read_config(module_folder="blueprints", module=bp_name)
                        if bp_config["init"]["share_models"]:
                            main.config["SHARED_MODELS"][bp_name] = import_object
                        show_stats(f":+ BLUEPRINT MODEL REGISTERED [{bp_name}.models] +:", live)
                    except AttributeError:
                        show_stats(
                            f":! ERROR REGISTERING BLUEPRINT MODEL [models.{bp_name}]: No import attribute found !:",
                            live)

        def load_extensions() -> None:
            for ex_name in load_modules(module_folder="extensions"):
                try:
                    extension_module = import_module(f"{app_name}.extensions.{ex_name}")
                    extension_object = getattr(extension_module, "bp")
                    main.register_blueprint(extension_object, name=f"{ex_name}")
                    show_stats(f":+ EXTENSION REGISTERED [{ex_name}] +:", live)
                except AttributeError:
                    show_stats(f":! ERROR REGISTERING EXTENSION [{ex_name}]: No import attribute found !:")
                    continue

                if path.isfile(f"{app_root}/extensions/{ex_name}/models.py"):
                    models_module = import_module(f"{app_name}.extensions.{ex_name}.models")
                    try:
                        import_object = getattr(models_module, "db")
                        import_object.init_app(main)
                        main.config["SHARED_MODELS"][ex_name] = import_object
                        show_stats(f":+ EXTENSION MODEL REGISTERED [{ex_name}.models] +:", live)
                    except AttributeError:
                        show_stats(
                            f":! ERROR REGISTERING EXTENSION MODEL [models.{ex_name}]: No import attribute found !:",
                            live)

        def load_apis() -> None:
            found_apis = load_modules(module_folder="api")
            for api_name in found_apis:
                try:
                    api_module = import_module(f"{app_name}.api.{api_name}")
                    api_object = getattr(api_module, "bp")
                    main.register_blueprint(api_object, name=f"api.{api_name}")
                    show_stats(f":+ API REGISTERED [{api_name}] +:", live)
                except AttributeError:
                    show_stats(f":! ERROR REGISTERING [{api_name}]: No import attribute found !:")
                    continue

        # Load Blueprints
        load_blueprints()
        load_extensions()
        load_apis()

        # Load builtins
        for route in import_routes(module_folder="builtins", module="routes"):
            import_module(f"{app_name}.builtins.routes.{route}")
        for route in import_routes(module_folder="builtins", module="extend_jinja"):
            import_module(f"{app_name}.builtins.extend_jinja.{route}")

        show_stats(rocket_launched(), live)

    return main
