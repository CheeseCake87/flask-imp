import logging
import os
import sys
from importlib import import_module
from inspect import getmembers
from inspect import isclass
from pathlib import Path
from typing import Dict, Union, Optional, List

from flask import Flask
from flask import Blueprint
from flask import session
from flask_sqlalchemy.model import DefaultMeta

from .helpers import init_app_config
from .registeries import ModelRegistry
from .utilities import cast_to_import_str


class BigApp:
    _app: Flask
    _app_name: str
    _app_path: Path
    _app_folder: Path
    _app_resources_imported: bool = False

    __model_registry__: ModelRegistry

    config_path: Path
    config: Dict

    def __init__(
            self,
            app: Optional[Flask] = None,
            app_config_file: Optional[str] = None,
            ignore_missing_env_variables: bool = False
    ) -> None:

        if app is not None:
            self.init_app(
                app,
                app_config_file,
                ignore_missing_env_variables
            )

    def init_app(
            self,
            app: Flask,
            app_config_file: Optional[str] = os.environ.get("BA_CONFIG"),
            ignore_missing_env_variables: bool = False
    ) -> None:

        """
        Initializes the flask app to work with flask-bigapp.

        :param app: The flask app to initialize.
        :param app_config_file: The config file to use.
        If not given will attempt to read from the environment.
        If no environment variable is found will use default.config.toml, which will be created if not found.
        :param ignore_missing_env_variables: If set to True will ignore missing environment variables.
        """

        if app is None:
            raise ImportError(
                "No app was passed in, do ba = BigApp(flaskapp) or app.init_app(flaskapp)")
        if not isinstance(app, Flask):
            raise TypeError(
                "The app that was passed in is not an instance of Flask")
        if app_config_file is None:
            app_config_file = "default.config.toml"

        self._app = app
        self._app_name = app.name
        self._app_path = Path(self._app.root_path)
        self._app_folder = self._app_path.parent
        self.config_path = self._app_path / app_config_file

        self.__model_registry__ = ModelRegistry()

        self.config = init_app_config(
            self.config_path,
            ignore_missing_env_variables,
            self._app
        )

    def import_app_resources(
            self,
            folder: str = "global",
            app_factories: Optional[List] = None,
            static_folder: str = "static",
            templates_folder: str = "templates",
            scope_root_folders_to: Optional[List] = None,
            scope_root_files_to: Optional[List] = None,
    ) -> None:
        """
        Import standard app resources from a single folder.

        :param folder: The folder to import from.
        Must be relative.
        :param app_factories: A list of function names to call with the app instance.
        ["collection"] => collection(app) will be called
        :param static_folder: The name of the static folder (if not found will be set to None)
        :param templates_folder: The name of the templates folder (if not found will be set to None)
        :param scope_root_folders_to: A list of folders to scope the import to
        ["cli", "routes"] => will only import from folder/cli/*.py and folder/routes/*.py
        :param scope_root_files_to: A list of files to scope the import to
        ["cli.py", "routes.py"] => will only import from folder/cli.py and folder/routes.py
        """

        if app_factories is None:
            app_factories = []

        if scope_root_folders_to is None:
            scope_root_folders_to = []

        if scope_root_files_to is None:
            scope_root_files_to = []

        if self._app_resources_imported:
            raise ImportError("The app resources can only be imported once.")

        self._app_resources_imported = True

        def process_module(import_location: str) -> tuple:
            module_file = import_module(import_location)
            flask_instance = True if [
                name for name, value in getmembers(module_file) if
                isinstance(value, Flask)
            ] else False

            return module_file, flask_instance

        skip_folders = ("static", "templates",)
        global_collection_folder = self._app_path / folder
        app_static_folder = global_collection_folder / static_folder
        app_templates_folder = global_collection_folder / templates_folder

        if not global_collection_folder.exists():
            raise ImportError(
                f"Cannot find global collection folder at {global_collection_folder}")

        if not global_collection_folder.is_dir():
            raise ImportError(
                f"Global collection must be a folder {global_collection_folder}")

        self._app.static_folder = app_static_folder.as_posix() if app_static_folder.exists() else None
        self._app.template_folder = app_templates_folder.as_posix() if app_templates_folder.exists() else None

        with self._app.app_context():
            for item in global_collection_folder.iterdir():

                if item.is_dir() and item.name not in skip_folders:
                    if scope_root_folders_to:
                        if item.name not in scope_root_folders_to:
                            continue

                    for py_file in item.glob("*.py"):
                        module, flask_instance_found = process_module(
                            f"{cast_to_import_str(self._app_name, item)}.{py_file.stem}")

                        for instance_factory in app_factories:
                            if hasattr(module, instance_factory):
                                getattr(module, instance_factory)(self._app)

                        if not flask_instance_found and not app_factories:
                            del sys.modules[module.__name__]

                if item.is_file() and item.suffix == ".py":
                    if scope_root_files_to:
                        if item.name not in scope_root_files_to:
                            continue

                    module, flask_instance_found = process_module(
                        cast_to_import_str(self._app_name, item))

                    for instance_factory in app_factories:
                        if hasattr(module, instance_factory):
                            getattr(module, instance_factory)(self._app)

                    if not flask_instance_found and not app_factories:
                        del sys.modules[module.__name__]

    def init_session(self) -> None:
        """
        Initialize the session variables found in the config.
        Use this method in the before_request route.
        """
        if self.config.get("SESSION"):
            for key, value in self.config.get("SESSION", {}).items():
                if key not in session:
                    session[key] = value

    def import_blueprint(self, blueprint: str) -> None:
        """
        Imports a single blueprint from the given path.

        :param blueprint: The blueprint (Python Package) to import.
        Must be relative.
        """
        if Path(blueprint).is_absolute():
            potential_bp = Path(blueprint)
        else:
            potential_bp = Path(self._app_path / blueprint)

        if potential_bp.exists() and potential_bp.is_dir():
            try:
                module = import_module(cast_to_import_str(self._app_name, potential_bp))
                for name, value in getmembers(module):
                    if isinstance(value, Blueprint):
                        if hasattr(value, "enabled"):
                            if value.enabled:
                                self._app.register_blueprint(value)
                            else:
                                logging.debug(f"Blueprint {name} is disabled")
                        else:
                            self._app.register_blueprint(value)
            except Exception as e:
                raise ImportError(f"Error when importing {potential_bp.name}: {e}")

    def import_blueprints(self, folder: str) -> None:
        """
        Imports all the blueprints in the given folder.

        :param folder: The folder to import from.
        Must be relative.
        """

        folder_path = Path(self._app_path / folder)

        for potential_bp in folder_path.iterdir():
            self.import_blueprint(potential_bp.as_posix())

    def import_models(
            self,
            file_or_folder: str
    ) -> None:
        """
        Imports all the models in the given file or folder.

        :param file_or_folder: The file or folder to import from.
        Must be relative.
        """

        def model_processor(path: Path):
            """
            Picks apart the model from_file and builds a registry of the models found.
            """
            import_string = cast_to_import_str(self._app_name, path)
            try:
                model_module = import_module(import_string)
                for name, value in getmembers(model_module, isclass):
                    if hasattr(value, "__tablename__"):
                        self.__model_registry__.add(name, value)

            except ImportError as e:
                raise ImportError(f"Error when importing {import_string}: {e}")

        if Path(file_or_folder).is_absolute():
            file_or_folder_path = Path(file_or_folder)
        else:
            file_or_folder_path = Path(self._app_path / file_or_folder)

        if file_or_folder_path.is_file() and file_or_folder_path.suffix == ".py":
            model_processor(file_or_folder_path)

        elif file_or_folder_path.is_dir():
            for model_file in [_ for _ in file_or_folder_path.iterdir() if "__" not in _.name]:
                model_processor(model_file)

    def model(self, class_: str) -> DefaultMeta:
        """
        Returns the model class for the given ORM class name

        bigapp.model("User") => <class 'app.models.User'>
        """
        return self.__model_registry__.class_(class_)

    def model_meta(self, class_: Union[str, DefaultMeta]) -> dict:
        """
        Returns meta information for the given ORM class name
        """

        def check_for_table_name(model_):
            if not hasattr(model_, "__tablename__"):
                raise AttributeError(f"{model_} is not a valid model")

        if isinstance(class_, str):
            model = self.__model_registry__.class_(class_)
            check_for_table_name(model)
            return {
                "location": model.__module__,
                "table_name": model.__tablename__,
            }

        return {
            "location": class_.__module__,
            "table_name": class_.__tablename__,
        }
