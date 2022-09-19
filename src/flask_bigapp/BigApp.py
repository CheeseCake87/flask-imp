import logging
import os
from importlib import import_module
from inspect import getmembers
from inspect import isclass
from os import listdir
from os import path
from sys import modules
from types import ModuleType

from flask import Flask
from flask import Blueprint
from flask import current_app
from flask_sqlalchemy import SQLAlchemy  # type: ignore

from typing import Dict, TextIO, Union, Optional

from .Blueprint import BigAppBlueprint
from .Config import Config
from .utilities import contains_illegal_chars


class BigApp(object):
    smtp: Dict = dict()
    structures: Dict = dict()
    model_classes: Dict = dict()

    _temp_config: Dict = dict()
    _app: Flask

    _default_config: Union[str, TextIO] = os.environ.get("BA_CONFIG", "default.config.toml")

    init_sqlalchemy = True
    db = None
    sql_do = None

    def __init__(
            self,
            app: Flask = None,
            init_sqlalchemy: bool = True,
            app_config_file: Optional[Union[str, TextIO, None]] = None
    ) -> None:
        if app is not None:
            self.init_app(app, init_sqlalchemy, app_config_file)

    def init_app(
            self,
            app: Flask,
            init_sqlalchemy: bool = True,
            app_config_file: Union[str, TextIO, None] = _default_config
    ) -> None:
        """
        Initializes the application.

        -> Expects a Flask application

        sqlalchemy object by default will be created unless init_sqlalchemy arg is set to False.

        Optional config file passed in. If no config file is given an
        attempt will be made to read from the environment for the variable BA_CONFIG
        If the environment variable is not found it will create a new config file
        called default.config.toml and proceed to load the values from there.
        """

        if app is None:
            raise ImportError("No app was passed in, do ... = BigApp(flaskapp) or ....init_app(flaskapp)")
        if not isinstance(app, Flask):
            raise TypeError("The app that was passed in is not an instance of a Flask app")

        self._app = app
        self.init_sqlalchemy = init_sqlalchemy

        if self.init_sqlalchemy:
            self.db = SQLAlchemy()
            self.sql_do = self.db.session

        config = Config(app, app_config_file)
        config.set_app_config()
        config.set_database_config()
        self.smtp = config.set_smtp_config()

    def import_builtins(self, folder: str = "routes") -> None:
        """
        Imports all the routes in the given folder.
        """
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
        """
        Imports all the blueprints in the given folder.
        """
        _imported_blueprints: Dict[str, ModuleType] = dict()

        with self._app.app_context():
            blueprints_raw, blueprints_clean = listdir(f"{current_app.root_path}/{folder}/"), []
            for blueprint in blueprints_raw:
                _path = f"{current_app.root_path}/{folder}/{blueprint}"
                if path.isdir(_path):
                    if not contains_illegal_chars(blueprint):
                        blueprints_clean.append(blueprint)

            for blueprint in blueprints_clean:
                _bp_root_folder: str = f"{current_app.root_path}/{folder}/{blueprint}"
                _bp_module_path: str = f"{current_app.name}.{folder.replace('/', '.')}.{blueprint}"
                try:
                    blueprint_module = import_module(_bp_module_path)
                    _imported_blueprints.update({_bp_module_path: blueprint_module})
                except AttributeError as e:
                    logging.critical("Error importing blueprint: ", e, f" from {_bp_module_path}")
                    continue

            for module_path, module in _imported_blueprints.items():
                for dir_item in dir(module):
                    if isinstance(getattr(module, dir_item), BigAppBlueprint):
                        instance_name: str = dir_item
                try:
                    blueprint_object = getattr(module, instance_name)
                    if blueprint_object.enabled:
                        current_app.register_blueprint(blueprint_object)
                except AttributeError as e:
                    logging.critical("Error importing blueprint: ", e, f" from {_bp_root_folder}")
                    continue

    def import_structures(self, structures_folder: str) -> None:
        """
        Imports all the structures in the given folder, this works the
        same as import_blueprints but does not require a config file and the
        settings are pulled from the environment of the folder.
        """
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
    def structure_tmpl(structure: str, template: Union[str, TextIO]) -> str:
        """
        pushes together a structure name to a template location.
        """
        return f"{structure}/{template}"

    def import_models(self, file: str = None, folder: str = None, import_attribute: str = "db") -> None:
        """
        Imports model files from a single file or a folder. Both are allowed to be set.

        You can also specify a different import attribute that you are using for your
        sqlalchemy object. A common one is db = SQLAlchemy(), so this is set as the default.
        """

        if file is None and folder is None:
            raise ImportError("You must pass in a file or folder located at the root of the app.")

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
                            getattr(_folder_model_module, import_attribute)
                        except ImportError as e:
                            logging.critical("Error importing model: ", e, f" from {folder_import_path}")
                            continue
                        except AttributeError as e:
                            logging.critical("Error importing model: ", e, f" from {folder_import_path}")
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
                        getattr(_file_model_module, import_attribute)

                    except ImportError as e:
                        logging.critical("Error importing model: ", e, f" from {file_import_path}")
                    except AttributeError as e:
                        logging.critical("Error importing model: ", e, f" from {file_import_path}")

                    file_model_members = getmembers(modules[file_import_path], isclass)
                    for file_member in file_model_members:
                        class_name = file_member[0]
                        class_object = file_member[1]
                        if current_app.name in str(class_object):
                            self.model_classes.update({class_name: class_object})

                else:
                    logging.info("Model file not found: ", f"{current_app.root_path}/{file}")

            "this is checking if the built in db initialization happened, if so it registers all the model files to it"
            if isinstance(self.db, SQLAlchemy):
                self.db.init_app(current_app)

        return

    def smtp_settings(self, email_address: str) -> dict:
        """
        Returns the SMTP settings for the given email address
        :param email_address:
        """
        if email_address in self.smtp:
            return self.smtp[email_address]
        return {}

    def model_class(self, class_name: str) -> ModuleType:
        """
        Returns the model class for the given class name
        :param class_name:
        """
        if class_name in self.model_classes:
            return self.model_classes[class_name]
        raise ValueError(f"{class_name} was not found in the list of model_classes")

    def create_all_models(self):
        if self.db is not None:
            with self._app.app_context():
                if isinstance(self.db, SQLAlchemy):
                    self.db.create_all()
                logging.info("All database models created.")
            return
        logging.warning("No database has been defined, you have likely chosen not to auto_init the database")
