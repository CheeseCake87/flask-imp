import logging
from importlib import import_module
from inspect import getmembers
from inspect import isclass
from os import listdir
from os import path
from sys import modules

from flask import Blueprint
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

from .Config import Config


class BigApp(object):
    smtp = dict()
    structures = dict()
    model_classes = dict()

    _temp_config = dict()
    _app = None

    db = None
    sql_do = None

    def __init__(self, app=None, app_config_file: str = None):
        if app is not None:
            self.init_app(app, app_config_file)

    def init_app(self, app, app_config_file: str):
        if app is None:
            raise ImportError("No app passed into BigApp")
        self._app = app

        config = Config(app, app_config_file)
        config.set_app_config()
        config.set_database_config()
        self.smtp = config.set_smtp_config()

    def import_builtins(self, folder: str = "routes") -> None:
        from .utilities import contains_illegal_chars

        with self._app.app_context():
            routes_raw, routes_clean = listdir(f"{current_app.root_path}/{folder}"), []
            for route in routes_raw:
                if contains_illegal_chars(route, exception=[".py"]):
                    continue
                routes_clean.append(route.replace(".py", ""))

            for route in routes_clean:
                try:
                    import_module(f"{current_app.name}.{folder.replace('/', '.')}.{route}")
                except ImportError as e:
                    logging.critical("Error importing builtin: ", e, f"in {folder}/{route}")
                    continue

    def import_blueprints(self, folder: str) -> None:
        from .utilities import contains_illegal_chars
        from .Blueprint import BigAppBlueprint

        _imported_blueprints = set()

        with self._app.app_context():
            blueprints_raw, blueprints_clean = listdir(f"{current_app.root_path}/{folder}/"), []
            for blueprint in blueprints_raw:
                _path = f"{current_app.root_path}/{folder}/{blueprint}"
                if path.isdir(_path):
                    if not contains_illegal_chars(blueprint):
                        blueprints_clean.append(blueprint)

            for blueprint in blueprints_clean:
                _bp_root_folder = f"{current_app.root_path}/{folder}/{blueprint}"
                try:
                    blueprint_module = import_module(f"{current_app.name}.{folder.replace('/', '.')}.{blueprint}")
                    _imported_blueprints.add(blueprint_module)
                except AttributeError as e:
                    logging.critical("Error importing blueprint: ", e, f" from {_bp_root_folder}")
                    continue

            for blueprint in _imported_blueprints:
                instance_name = None
                for value in dir(blueprint):
                    if isinstance(getattr(blueprint, value), BigAppBlueprint):
                        instance_name = value
                try:
                    blueprint_object = getattr(blueprint, instance_name)
                    if blueprint_object.enabled:
                        current_app.register_blueprint(blueprint_object)
                except AttributeError as e:
                    logging.critical("Error importing blueprint: ", e, f" from {_bp_root_folder}")
                    continue

    def import_structures(self, structures_folder: str) -> None:
        from .utilities import contains_illegal_chars

        with self._app.app_context():
            structures_raw, structures_clean = listdir(f"{current_app.root_path}/{structures_folder}/"), []
            dunder_name = __name__
            split_dunder_name = dunder_name.split(".")

            for structure in structures_raw:
                _path = f"{current_app.root_path}/{structures_folder}/{structure}"
                if path.isdir(_path):
                    if not contains_illegal_chars(structure):
                        structures_clean.append(structure)

            for structure in structures_clean:
                _structure_root_folder = f"{current_app.root_path}/{structures_folder}/{structure}"
                self.structures.update({structure: _structure_root_folder})
                bp = Blueprint(
                    name=structure,
                    import_name=f"{split_dunder_name[0]}/{structures_folder}/{structure}",
                    static_folder=f"{current_app.root_path}/{structures_folder}/{structure}/static",
                    template_folder=f"{current_app.root_path}/{structures_folder}/{structure}/templates",
                    static_url_path=f"/{structure}/static"
                )
                current_app.register_blueprint(bp)

    @staticmethod
    def structure_tmpl(structure, template):
        return f"{structure}/{template}"

    def import_models(self, file: str = None, folder: str = None, import_attribute: str = "db", auto_init: bool = True) -> None:
        from .utilities import contains_illegal_chars

        if file is None and folder is None:
            raise ImportError("You must pass in a file or folder located at the root of the app.")

        if auto_init:
            self.db = SQLAlchemy()
            self.sql_do = self.db.session

        with self._app.app_context():
            if folder is not None:
                _folder = f"{current_app.root_path}/{folder}"
                if path.isdir(_folder):
                    folder_models_raw, folder_modules_clean = listdir(_folder), []
                    for model in folder_models_raw:
                        if contains_illegal_chars(model, exception=[".py"]):
                            continue
                        folder_modules_clean.append(model.replace(".py", ""))

                    for folder_model in folder_modules_clean:
                        split_folder = _folder.split("/")
                        strip_folder = split_folder[split_folder.index(current_app.name):]
                        folder_import_path = f"{'.'.join(strip_folder)}.{folder_model}"
                        try:
                            _folder_model_module = import_module(folder_import_path)
                            _folder_model_object = getattr(_folder_model_module, import_attribute)

                        except ImportError as e:
                            print("Error importing model: ", e, f" from {folder_import_path}")
                            continue
                        except AttributeError as e:
                            print("Error importing model: ", e, f" from {folder_import_path}")
                            continue

                        folder_model_members = getmembers(modules[folder_import_path], isclass)
                        for folder_member in folder_model_members:
                            class_name = folder_member[0]
                            class_object = folder_member[1]
                            if current_app.name in str(class_object):
                                self.model_classes.update({class_name: class_object})
                else:
                    logging.info("Model folder not found: ", f"{current_app.root_path}/{folder}")

            if file is not None:
                _file = f"{current_app.root_path}/{file}"
                if path.isfile(_file):
                    split_file = _file.split("/")
                    strip_file = split_file[split_file.index(current_app.name):]
                    file_import_path = f"{'.'.join(strip_file)}.{file}"
                    try:
                        _file_model_module = import_module(file_import_path)
                        _file_model_object = getattr(_file_model_module, import_attribute)

                    except ImportError as e:
                        print("Error importing model: ", e, f" from {file_import_path}")
                    except AttributeError as e:
                        print("Error importing model: ", e, f" from {file_import_path}")

                    file_model_members = getmembers(modules[file_import_path], isclass)
                    for file_member in file_model_members:
                        class_name = file_member[0]
                        class_object = file_member[1]
                        if current_app.name in str(class_object):
                            self.model_classes.update({class_name: class_object})

                else:
                    logging.info("Model file not found: ", f"{current_app.root_path}/{file}")

            if auto_init:
                self.db.init_app(current_app)

    def smtp_settings(self, email_address: str) -> dict:
        if email_address in self.smtp:
            return self.smtp[email_address]

    def model_class(self, class_name: str):
        return self.model_classes[class_name]

    def create_all_models(self):
        if self.db is not None:
            with self._app.app_context():
                self.db.create_all()
                logging.info("All database models created.")
            return
        logging.warning("No database has been defined, you have likely chosen not to auto_init the database")
