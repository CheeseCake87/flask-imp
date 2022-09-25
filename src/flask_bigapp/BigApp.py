import logging
import os
import pathlib
import re
from importlib import import_module
from inspect import getmembers
from inspect import isclass
from types import ModuleType
from typing import Dict, TextIO, Union, Optional, Any
from toml import load

from flask import Blueprint
from flask import Flask
from flask import current_app
from flask_sqlalchemy import SQLAlchemy  # type: ignore

from .Blueprint import BigAppBlueprint
from .Resources import Resources


class BigApp(object):
    smtp: Dict = dict()
    structures: Dict = dict()
    model_classes: Dict = dict()
    db = None
    sql_do = None

    __config: Dict = dict()
    __app: Flask
    __app_name: str
    __app_path: pathlib.PurePath
    __app_folder: str

    __default_config: Union[str, bytes, os.PathLike, None] = os.environ.get("BA_CONFIG", None)

    def __init__(
            self,
            app: Flask = None,
            sqlalchemy_db: Optional[Union[SQLAlchemy, None]] = None,
            app_config_file: Optional[Union[str, bytes, os.PathLike, None]] = None
    ) -> None:
        if app is not None:
            self.init_app(app, sqlalchemy_db, app_config_file)

    def init_app(
            self,
            app: Flask,
            sqlalchemy_db: Union[SQLAlchemy, None] = None,
            app_config_file: Union[str, bytes, os.PathLike, None] = __default_config
    ) -> None:
        """
        Initializes the application.

        -> Expects a Flask application

        Can be passed an SQLAlchemy object, doing this will enable the use of the model_class.

        Optional config file passed in. If no config file is given an
        attempt will be made to read from the environment for the variable BA_CONFIG
        If the environment variable is not found it will create a new config file
        called default.config.toml and proceed to load the values from there.
        """

        if app is None:
            raise ImportError("No app was passed in, do ... = BigApp(flaskapp) or ....init_app(flaskapp)")
        if not isinstance(app, Flask):
            raise TypeError("The app that was passed in is not an instance of a Flask app")

        self.__app = app
        self.__app_name = app.name
        self.__app_path = pathlib.PurePath(self.__app.root_path)
        self.__app_folder = self.__app_path.parts[-1]
        self.__config = self.__load_config_file(app_config_file)
        self.__config_processor(self.__config)

        self.db = sqlalchemy_db

        if isinstance(self.db, SQLAlchemy):
            self.sql_do = self.db.session

    def import_builtins(self, folder: Union[Any, os.PathLike] = "routes") -> None:
        """
        Imports all the routes in the given folder.

        Folder must be relative ( folder="here" not folder="/home/user/app/folder" )
        """
        folder_path = pathlib.Path(pathlib.PurePath(self.__app_path) / folder)
        location_parts_reversed = tuple(reversed(folder_path.parts))
        shrink_parts_to_app = location_parts_reversed[:location_parts_reversed.index(self.__app_name) + 1]
        if folder_path.is_dir():
            builtin_files = folder_path.glob("*.py")
            with self.__app.app_context():
                for builtin in builtin_files:
                    import_module(f"{'.'.join(tuple(reversed(shrink_parts_to_app)))}.{builtin.stem}")

    def import_blueprints(self, folder: Union[Any, os.PathLike]) -> None:
        """
        Imports all the blueprints in the given folder.

        Folder must be relative ( folder="here" not folder="/home/user/app/folder" )
        """

        folder_path = pathlib.Path(pathlib.PurePath(self.__app_path) / folder)
        blueprints_found = folder_path.iterdir()

        blueprints_register: Dict[str, ModuleType] = dict()
        for blueprint in blueprints_found:
            location_parts_reversed = tuple(reversed(blueprint.parts))
            shrink_parts_to_app = location_parts_reversed[:location_parts_reversed.index(self.__app_name) + 1]
            try:
                import_blueprint_module = import_module(".".join(tuple(reversed(shrink_parts_to_app))))
                blueprints_register.update({blueprint.name: import_blueprint_module})
                for dir_item in dir(import_blueprint_module):
                    if isinstance(getattr(import_blueprint_module, dir_item), BigAppBlueprint):
                        try:
                            blueprint_object = getattr(import_blueprint_module, dir_item)
                            if blueprint_object.enabled:
                                self.__app.register_blueprint(blueprint_object)
                        except AttributeError as e:
                            logging.critical("Error importing blueprint: ", e, f"{blueprint.name}")
            except AttributeError as e:
                logging.critical("Error importing blueprint: ", e, f" from {folder_path}")
                continue

    def import_structures(self, structures_folder: Union[Any, os.PathLike]) -> None:
        """
        Imports all the structures in the given folder, this works the
        same as import_blueprints but does not require a config file. The
        settings are pulled from the environment of the folder.

        Folder must be relative ( folder="here" not folder="/home/user/app/folder" )
        """

        folder_path = pathlib.Path(pathlib.PurePath(self.__app_path) / structures_folder)
        structures_folder_files = folder_path.iterdir()

        structures_register: Dict[str, ModuleType] = dict()
        for structure in structures_folder_files:
            location_parts_reversed = tuple(reversed(structure.parts))
            shrink_parts_to_app = location_parts_reversed[:location_parts_reversed.index(self.__app_name) + 1]
            try:
                import_structure_module = import_module(".".join(tuple(reversed(shrink_parts_to_app))))
                structures_register.update({structure.name: import_structure_module})
                structure_blueprint = Blueprint(
                    name=structure.name,
                    import_name=f"{structure.name}",
                    static_folder=f"{structure.absolute()}/static",
                    template_folder=f"{structure.absolute()}/templates",
                    static_url_path=f"/{structure.name}/static"
                )
                self.__app.register_blueprint(structure_blueprint)
            except AttributeError as e:
                logging.critical("Error importing blueprint: ", e, f" from {folder_path}")
                continue

    def import_models(
            self,
            file: Optional[Union[Any, os.PathLike]] = None,
            folder: Optional[Union[Any, os.PathLike]] = None
    ) -> None:
        """
        Imports model files from a single file or a folder. Both are allowed to be set.

        File and Folder must be relative ( folder="here" not folder="/home/user/app/folder" )
        """
        if file is None and folder is None:
            raise ImportError("You must pass in a file or folder located at the root of the app.")

        if folder is not None:
            folder_path = pathlib.Path(pathlib.PurePath(self.__app_path) / folder)
            if folder_path.is_dir():
                model_files = folder_path.glob("*.py")
                for model_file in model_files:
                    self.__import_model_processor(model_file)

        if file is not None:
            file_path = pathlib.Path(pathlib.PurePath(self.__app_path) / file)
            if file_path.is_file() and file_path.suffix == ".py":
                self.__import_model_processor(file_path)

        "this is checking if the built in db initialization happened, if so it registers all the model files to it"
        if isinstance(self.db, SQLAlchemy):
            with self.__app.app_context():
                self.db.init_app(current_app)
        return

    def model_class(self, class_name: str) -> ModuleType:
        """
        Returns the model class for the given class name

        table_class = bigapp.model_class("ExampleTable")
        table_query = table_class.query.all()
        """
        if class_name in self.model_classes:
            return self.model_classes[class_name]
        raise ValueError(f"{class_name} was not found in the list of model_classes")

    def get_smtp_settings(self, email_address: str) -> dict:
        """
        Returns the SMTP settings from the config for the given email address

        email = bigapp.get_smtp_settings("example@example.com")
        email_server = email['server']
        """
        if email_address in self.smtp:
            return self.smtp[email_address]
        return {}

    def __load_config_file(self, config_file: Union[Any, os.PathLike]) -> Dict:
        """
        Attempts to load the passed in config file, if no config file is passed in
        an attempt will be made to first read the default config file. If this fails
        an attempt will be made to create a default config file, then read it.
        """
        config_suffix = ('.toml', '.tml')

        if config_file is not None:
            passed_config = self.__app_path / config_file
            if pathlib.Path(passed_config).is_file() and passed_config.suffix in config_suffix:
                return load(passed_config)

        default_config = pathlib.PurePath(self.__app_path / "default.config.toml")
        if pathlib.Path(default_config).is_file():
            return load(default_config)

        create_default_config = pathlib.Path(default_config)
        create_default_config.touch()
        create_default_config.write_text(Resources.default_config)

        return load(create_default_config)

    def __config_processor(self, config: Dict):
        """
        Processes the values from the configuration file.
        """
        flask_config = config.get("flask")
        database_config = config.get("database")
        smtp_config = config.get("smtp")

        if flask_config is not None and isinstance(flask_config, dict):
            if flask_config.get("static_folder", False):
                self.__app.static_folder = self.__if_env_replace(flask_config.get("static_folder"))
                del flask_config['static_folder']
            if flask_config.get("template_folder", False):
                self.__app.template_folder = self.__if_env_replace(flask_config.get("template_folder"))
                del flask_config['template_folder']
            for __key, __value in flask_config.items():
                self.__app.config.update({str(__key).upper(): self.__if_env_replace(__value)})

        if database_config is not None and isinstance(database_config, dict):
            self.__app.config['SQLALCHEMY_BINDS'] = dict()
            for __key, __value in database_config.items():
                if __value.get("enabled", False):
                    if __key == "main":
                        self.__app.config['SQLALCHEMY_DATABASE_URI'] = f"{self.__build_database_uri(__value)}"
                    self.__app.config['SQLALCHEMY_BINDS'].update({__key: f"{self.__build_database_uri(__value)}"})

        if smtp_config is not None and isinstance(smtp_config, dict):
            for __key, __value in smtp_config.items():
                this_key = self.__if_env_replace(__key)
                self.smtp.update({this_key: Dict[str, Any]})
                for ___key, ___value in __value.items():
                    self.smtp[this_key].update({___key: self.__if_env_replace(___value)})

    def __import_model_processor(self, path: pathlib.PurePath):
        """
        Picks apart the model file and builds a registry of the models found.
        """
        # Reverse the path to find the first index of the app name, incase any parent dir has the same name.
        folder_location_parts_reversed = tuple(reversed(path.parts))
        folder_shrink_parts_to_app = folder_location_parts_reversed[:folder_location_parts_reversed.index(self.__app_name) + 1]
        module_import_path = ".".join(tuple(reversed(folder_shrink_parts_to_app))).replace(".py", "")
        try:
            model_module = import_module(module_import_path)
            for model_object_members in getmembers(model_module, isclass):
                if module_import_path in model_object_members[1].__module__:
                    self.model_classes.update({
                        model_object_members[0]: model_object_members[1]
                    })
        except ImportError as e:
            logging.critical("Error importing model: ", e, f" {module_import_path}")

    def __build_database_uri(self, block: dict) -> str:
        """
        Puts together the correct database URI depending on the type specified.

        Fails if type is not supported.
        """
        db_type = block.get("type")
        db_location = block.get("location")

        db_allowed = ('postgresql', 'mysql', 'oracle')

        if db_type == "sqlite":
            final_location = self.__app_path
            if db_location is not None:
                final_location = final_location / db_location
            return f"{db_type}:////{final_location}/{block.get('database_name', 'database')}.sqlite"

        if db_type in db_allowed:
            return f"{db_type}://{block.get('username', 'None')}:{block.get('password', 'None')}" \
                   f"@{block.get('location', 'None')}:{str(block.get('port', 'None'))}/" \
                   f"{block.get('database_name', 'None')}"

        raise ValueError(f"Unknown database type: {db_type}, must be: postgresql / mysql / oracle / sqlite")

    @staticmethod
    def __if_env_replace(value: Optional[Any]) -> Any:
        """
        Looks for the replacement pattern to swap out values in the config file with environment variables.
        """
        pattern = re.compile(r'<(.*?)>')

        if isinstance(value, str):
            if re.match(pattern, value):
                env_var = re.findall(pattern, value)[0]
                return os.environ.get(env_var, "ENV_KEY_NOT_FOUND")
        return value

    @staticmethod
    def structure_tmpl(structure: str, template: Union[str, TextIO]) -> str:
        """
        pushes together a structure name to a template location.
        """
        return f"{structure}/{template}"
