from .builtins.functions.email import test_email_server_connection
from .builtins.functions.email import send_email
from .builtins.functions.import_mgr import show_stats
from .builtins.functions.import_mgr import load_config
from .builtins.functions.import_mgr import load_modules
from .builtins.functions.import_mgr import import_routes
from .builtins.functions.utilities import building_rocket
from .builtins.functions.utilities import rocket_launched
from .builtins.functions.utilities import email_server_status
from importlib import import_module
from datetime import timedelta
from flask import Flask
from os import path

settings = load_config(app_config=True)
app_name = settings["app"]["name"]
app_root = settings["app"]["root"]


class Config(object):
    APP_NAME = app_name
    SECRET_KEY = settings["app"]["secret_key"]
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=int(settings["app"]["session_time"]))
    DEBUG = settings["app"]["debug"]
    TESTING = settings["app"]["testing"]
    UPLOAD_FOLDER = f"{app_root}/uploads"
    if settings["database"]["enabled"]:
        _db = settings["database"]["name"]
        _u = settings["database"]["username"]
        _p = settings["database"]["password"]
        if settings["database"]["type"] == "sqlite":
            SQLALCHEMY_DATABASE_URI = f"{settings['database']['type']}:///{app_root}/database.db"
        else:
            SQLALCHEMY_DATABASE_URI = f"{settings['database']['type']}://{_u}:{_p}@localhost/{_db}"
        SQLALCHEMY_TRACK_MODIFICATIONS = True


def create_app() -> object:
    main = Flask(__name__)
    main.config.from_object(Config)
    main.template_folder = settings["app"]["template_folder"]
    main.static_folder = settings["app"]["static_folder"]

    print(building_rocket())
    print(f">> {settings['frameworks']['launchpad']}")
    email_server_probe = test_email_server_connection()
    if email_server_probe[0]:
        print(email_server_status(email_server_probe[0], email_server_probe[1]))
    else:
        print(email_server_status(email_server_probe[0], email_server_probe[1]))

    show_stats(f":: GLOBAL JS : {settings['frameworks']['global_js']} ::")
    show_stats(f":: GLOBAL CSS : {settings['frameworks']['global_css']} ::")

    with main.app_context():
        def load_blueprints() -> None:
            for bp_name in load_modules(module_folder="blueprints"):
                try:
                    blueprint_module = import_module(f"{app_name}.blueprints.{bp_name}")
                    blueprint_object = getattr(blueprint_module, "bp")
                    main.register_blueprint(blueprint_object, name=f"{bp_name}")
                    show_stats(f":+ BLUEPRINT REGISTERED [{bp_name}] +:")
                except AttributeError:
                    show_stats(f":! ERROR REGISTERING BLUEPRINT [{bp_name}]: No import attribute found !:")
                    continue

                if path.isfile(f"{app_root}/blueprints/{bp_name}/models.py"):
                    models_module = import_module(f"{app_name}.blueprints.{bp_name}.models")
                    try:
                        import_object = getattr(models_module, "db")
                        import_object.init_app(main)
                        show_stats(f":+ MODEL REGISTERED [{bp_name}.models] +:")
                    except AttributeError:
                        show_stats(f":! ERROR REGISTERING MODEL [models.{bp_name}]: No import attribute found !:")

        def load_apis() -> None:
            found_apis = load_modules(module_folder="apis")
            for api_name in found_apis:
                found_api_routes = import_routes(module_folder="apis", module=api_name)

                for route in found_api_routes:
                    api_route_module = import_module(f"{app_name}.apis.{api_name}.routes.{route}")
                    try:
                        import_object = getattr(api_route_module, "api")
                        import_object.init_app(main)
                        show_stats(f":+ API ROUTES REGISTERED [{api_name}.{route}] +:")
                    except AttributeError:
                        show_stats(
                            f":! ERROR REGISTERING ROUTE [{api_name}.{route}]: No import attribute found !:")

                if path.isfile(f"{app_root}/apis/{api_name}/models.py"):
                    models_module = import_module(f"{app_name}.apis.{api_name}.models")
                    try:
                        import_object = getattr(models_module, "db")
                        import_object.init_app(main)
                        show_stats(f":+ MODEL REGISTERED [{api_name}] +:")
                    except AttributeError:
                        show_stats(f":! ERROR REGISTERING MODEL [{api_name}]: No import attribute found !:")

        load_apis()
        load_blueprints()
        show_stats(" ")
        from .builtins.extend_jinja import filters
        show_stats(":+ BUILTIN CUSTOM JINJA FILTERS LOADED +:")
        from .builtins.routes import __pre_post__
        show_stats(":+ BUILTIN ROUTE REGISTERED [builtin___pre_post__] +:")
        from .builtins.routes import errors
        show_stats(":+ BUILTIN ROUTE REGISTERED [errors] +:")
        from .builtins.routes import system
        show_stats(":+ BUILTIN ROUTE REGISTERED [system] +:")
        show_stats("!! VISIT <url>/system/endpoints TO GET A LIST OF ENDPOINTS !!")
        print(rocket_launched())
        print(" ")
    return main
