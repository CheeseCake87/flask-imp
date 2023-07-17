import logging
import os
from importlib import import_module
from inspect import getmembers
from inspect import isclass
from pathlib import Path
from typing import Dict, Union, Optional

from flask import Flask
from flask import session
from flask_sqlalchemy.model import DefaultMeta

from .blueprint import BigAppBlueprint
from .helpers import init_app_config
from .registeries import ModelRegistry
from .utilities import cast_to_import_str


class BigApp:
    _app: Flask
    _app_name: str
    _app_path: Path
    _app_folder: Path
    _global_collection_imported: bool = False

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
        Initializes the application.

        -> Expects a Flask application

        Can be passed an SQLAlchemy object, doing this will enable the use of the model_class.

        Optional config from_file passed in. If no config from_file is given an
        attempt will be made to read from the environment for the variable BA_CONFIG
        If the environment variable is not found it will create a new config from_file
        called default.config.toml and proceed to load the values from there.
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

    def import_global_collection(self) -> None:
        """
        Will look in the root of the app for a folder called global.
        """
        if self._global_collection_imported:
            logging.warning(
                "The global collection has already been imported, skipping")
            return

        self._global_collection_imported = True

        skip_folders = ("static", "templates",)
        global_collection_folder = self._app_path / "global"
        if global_collection_folder.is_dir():
            self._app.template_folder = global_collection_folder / "templates"
            self._app.static_folder = "global/static"
            with self._app.app_context():
                for folder in global_collection_folder.iterdir():
                    if folder.is_dir() and folder.name not in skip_folders:
                        for py_file in folder.glob("*.py"):
                            module_file = import_module(
                                f"{cast_to_import_str(self._app_name, folder)}.{py_file.stem}"
                            )
                            if hasattr(module_file, "collection"):
                                module_file.collection(self._app)

    def init_session(self) -> None:
        """
        Initialize the session variables found in the config from_file.
        Use this method in the before_request route.
        """
        if self.config.get("SESSION"):
            for key, value in self.config.get("SESSION", {}).items():
                if key not in session:
                    session[key] = value

    def import_blueprint(self, blueprint: Union[str, Path]):
        """
        Imports a single blueprint from the given path.

        Path must be relative ( path="here" not path="/home/user/app/from_folder" )
        """
        if isinstance(blueprint, str):
            potential_bp = Path(self._app_path / blueprint)
        else:
            potential_bp = blueprint

        if potential_bp.is_dir():
            try:
                module = import_module(cast_to_import_str(self._app_name, potential_bp))
                for dir_item in dir(module):
                    _ = getattr(module, dir_item)
                    if isinstance(_, BigAppBlueprint):
                        if _.enabled:
                            self._app.register_blueprint(_)
                        break
            except Exception as e:
                logging.critical(f"{e}",
                                 f"Error importing blueprint: from {potential_bp}")

    def import_blueprints(self, folder: str) -> None:
        """
        Imports all the blueprints in the given from_folder.

        Folder must be relative ( from_folder="here" not from_folder="/home/user/app/from_folder" )
        """

        folder_path = Path(self._app_path / folder)

        for potential_bp in folder_path.iterdir():
            self.import_blueprint(potential_bp)

    def import_models(
            self,
            from_file: Optional[Union[str, Path]] = None,
            from_folder: Optional[Union[str, Path]] = None,
    ) -> None:
        """
        Imports model files from a single from_file or a from_folder.
        Both are allowed to be set.

        File and Folder must be relative
        ( from_folder="here" not from_folder="/home/user/app/from_folder" )
        """

        def model_processor(path: Path):
            """
            Picks apart the model from_file and builds a registry of the models found.
            """
            import_string = cast_to_import_str(self._app_name, path)
            try:
                model_module = import_module(import_string)
                for model_object_members in getmembers(model_module, isclass):
                    if import_string in model_object_members[1].__module__:
                        name = model_object_members[0]
                        model = model_object_members[1]
                        if not hasattr(model, "__tablename__"):
                            raise AttributeError(
                                f"{name} is not a valid model")

                        self.__model_registry__.add(name, model)

            except ImportError as e:
                logging.critical("Error importing model: ", e, f" {import_string}")

        if from_file is None and from_folder is None:
            raise ImportError(
                "No model from_file or from_folder was passed in")

        if from_file is not None:
            if isinstance(from_file, Path):
                file_path = from_file
            else:
                file_path = Path(self._app_path / from_file)

            if file_path.is_file() and file_path.suffix == ".py":
                model_processor(file_path)
            else:
                from_folder = from_file

        if from_folder is not None:
            if isinstance(from_folder, Path):
                folder_path = from_folder
            else:
                folder_path = Path(self._app_path / from_folder)

            if folder_path.is_dir():
                for model_file in folder_path.glob("*.py"):
                    if "__" in model_file.name:
                        continue
                    model_processor(model_file)

    def model(self, class_: str) -> DefaultMeta:
        """
        Returns the model class for the given ORM class name
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
