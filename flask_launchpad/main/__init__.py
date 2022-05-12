from importlib import import_module
from datetime import timedelta
from flask import Flask
from flask import Blueprint
from .flask_launchpad import FlaskLaunchpad
from os import path

from .builtins.functions.email_connector import test_email_server_connection
from .builtins.functions.email_connector import send_email
from .builtins.functions.import_mgr import show_stats
from .builtins.functions.import_mgr import read_config_as_dict
from .builtins.functions.import_mgr import read_nav
from .builtins.functions.import_mgr import load_modules
from .builtins.functions.import_mgr import import_routes
from .builtins.functions.utilities import building_rocket
from .builtins.functions.utilities import rocket_launched
from .builtins.functions.utilities import email_server_status
from .builtins.functions.utilities import create_folder_if_not_found

settings = read_config_as_dict(app_config=True)
app_name = settings["app"]["name"]
app_root = settings["app"]["root"]

fl = FlaskLaunchpad()


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
    HOME_PAGE = settings["app"]["home_page"]
    LOGIN_DASHBOARD = settings["app"]["login_dashboard"]
    SHARED_MODELS = {}
    BACKEND_NAV = {}
    FRONTEND_NAV = {}
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
    create_folder_if_not_found(main.config["UPLOAD_FOLDER"])

    fl.init_app(main)

    fl.import_blueprints("blueprints")
    fl.import_blueprints("extensions")

    for rule in main.url_map.iter_rules():
        print(rule)

    return main
