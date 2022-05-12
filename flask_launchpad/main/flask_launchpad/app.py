from flask import current_app
from flask import Blueprint
from importlib import import_module
from os import path
from os import listdir
from configparser import ConfigParser

from .utilities.import_mgr import load_modules


class FlaskLaunchpad(object):
    def __init__(self, app=None):
        self._app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app=None):
        if app is None:
            raise ImportError
        self._app = app

    def register_structure_folder(self, folder: str) -> None:
        """
        Registers a folder in the root path as a Flask template folder.

        For more info see: https://uilix.com/flask-launchpad/#register_structure_folder

        :param folder: str
        :return: None
        """
        with self._app.app_context():
            structures = Blueprint(folder, folder, template_folder=f"{current_app.root_path}/{folder}")
            current_app.register_blueprint(structures)

    def import_blueprints(self, folder: str):
        """
        Looks through the passed in folder for Blueprint modules, imports them then registers them with Flask.

        The Blueprint object must be stored in a variable called bp in the __init__.py file, for example:

        bp = Blueprint(settings)

        For more info see: https://uilix.com/flask-launchpad/#import_blueprints

        :param folder: str
        :return: None
        """

        def find_illegal_dir_char(name: str) -> bool:
            """
            Removes illegal chars from dir
            """
            illegal_characters = ['%', '$', '£', ' ', '#', 'readme', '__', '.py']
            for char in illegal_characters:
                if char in name:
                    return True
            return False

        with self._app.app_context():
            blueprints_raw, blueprints_clean = listdir(f"{current_app.root_path}/{folder}/"), []
            for blueprint in blueprints_raw:
                if path.isdir(f"{current_app.root_path}/{folder}/{blueprint}"):
                    blueprints_clean.append(blueprint)

            for blueprint in blueprints_clean:
                if "config.ini" in listdir(f"{current_app.root_path}/{folder}/{blueprint}/"):
                    blueprint_config = ConfigParser()
                    blueprint_config.read(f"{current_app.root_path}/{folder}/config.ini")
                    if "init" in blueprint_config:
                        if "enabled" in blueprint_config["init"]:
                            print(blueprint, "enabled found")
                            if not blueprint_config.getboolean("init", "enabled"):
                                print(blueprint, "disabled")
                                continue
                try:
                    blueprint_module = import_module(f"{current_app.name}.{folder}.{blueprint}")
                    blueprint_object = getattr(blueprint_module, "bp")
                    current_app.register_blueprint(blueprint_object, name=f"{blueprint}")
                except AttributeError:
                    continue

                bp_root_folder = f"{current_app.root_path}/{folder}/{blueprint}"

                routes_raw, routes_clean = listdir(f"{bp_root_folder}/routes"), []
                for route in routes_raw:
                    if find_illegal_dir_char(route):
                        continue
                    routes_clean.append(route.replace(".py", ""))

                for route in routes_clean:
                    try:
                        import_module(f"{current_app.name}.{folder}.{blueprint}.routes.{route}")
                    except ImportError:
                        print()
                        continue

                if path.isfile(f"{bp_root_folder}/models.py"):
                    models_module = import_module(f"{current_app.name}.{folder}.{blueprint}.models")
                    try:
                        import_object = getattr(models_module, "db")
                        import_object.init_app(current_app)
                    except AttributeError:
                        continue

    # def connect(self):
    #     return sqlite3.connect(current_app.config['SQLITE3_DATABASE'])

    def teardown(self, exception):
        pass
        # ctx = _app_ctx_stack.top
        # if hasattr(ctx, 'sqlite3_db'):
        #     ctx.sqlite3_db.close()

    # @property
    # def connection(self):
    #     ctx = _app_ctx_stack.top
    #     if ctx is not None:
    #         if not hasattr(ctx, 'sqlite3_db'):
    #             ctx.sqlite3_db = self.connect()
    #         return ctx.sqlite3_db


class StructureBuilder:
    def __init__(self):
        pass
