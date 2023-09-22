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

from .helpers import _init_app_config
from .registeries import ModelRegistry
from .utilities import cast_to_import_str


class Imp:
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
            app_config_file: Optional[str] = os.environ.get("IMP_CONFIG"),
            ignore_missing_env_variables: bool = False
    ) -> None:

        """
        Initializes the flask app to work with flask-imp.
        
        :raw-html:`<br />`
        
        If no `app_config_file` specified, an attempt to read `IMP_CONFIG` from the environment will be made.

        :raw-html:`<br />`

        If `IMP_CONFIG` is not in the environment variables, an attempt to load `default.config.toml` will be made.

        :raw-html:`<br />`

        `default.config.toml` will be created, and used if not found.

        :raw-html:`<br />`

        -----

        :param app: The flask app to initialize.
        :param app_config_file: The config file to use.
        :param ignore_missing_env_variables: Will ignore missing environment variables in the config if set to True.
        :return: None
        """

        if app is None:
            raise ImportError(
                "No app was passed in, do ba = Imp(flaskapp) or app.init_app(flaskapp)")
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

        self.config = _init_app_config(
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
        Import standard app resources from the specified folder.

        :raw-html:`<br />`

        This will import any resources that have been set to the Flask app. Routes, context processors, cli, etc.

        :raw-html:`<br />`

        **Can only be called once.**

        :raw-html:`<br />`

        If no static folder is found, the static folder will be set to None in the Flask app config.

        :raw-html:`<br />`

        **Small example of usage:**

        :raw-html:`<br />`

        .. code-block:: text

            imp.import_app_resources(folder="global")

        ...
        :raw-html:`<br />`

        ---
        `global` folder structure
        ---

        .. code-block:: text

            app
            ├── global
            │   ├── routes.py
            │   ├── app_fac.py
            │   ├── static
            │   │   └── css
            │   │       └── style.css
            │   └── templates
            │       └── index.html
            └── ...
        ...
        :raw-html:`<br />`

        ---
        `routes.py` file
        ---

        .. code-block::

            from flask import current_app as app
            from flask import render_template

            @app.route("/")
            def index():
                return render_template("index.html")

        :raw-html:`<br />`

        **How app app_factories work**

        :raw-html:`<br />`

        app_factories are functions that are called when importing the app resources. Here's an example:

        :raw-html:`<br />`

        .. code-block::

            imp.import_app_resources(folder="global", app_factories=["development_cli"])

        :raw-html:`<br />`

        ["development_cli"] => development_cli(app) function will be called, and the current app will be passed in.

        :raw-html:`<br />`

        --- `app_fac.py` file ---

        .. code-block::

            def development_cli(app):
                @app.cli.command("dev")
                def dev():
                    print("dev cli command")

        :raw-html:`<br />`

        **How to scope the import**

        :raw-html:`<br />`

        scope_root_folders_to=["cli", "routes"] => will only import files from `<folder>/cli/*.py`
        and `<folder>/routes/*.py`

        :raw-html:`<br />`

        scope_root_files_to=["cli.py", "routes.py"] => will only import the files `<folder>/cli.py`
        and `<folder>/routes.py`

        :raw-html:`<br />`

        -----

        :param folder: The folder to import from, must be relative.
        :param app_factories: A list of function names to call with the app instance.
        :param static_folder: The name of the static folder (if not found will be set to None)
        :param templates_folder: The name of the templates folder (if not found will be set to None)
        :param scope_root_folders_to: A list of folders to scope the import to
        :param scope_root_files_to: A list of files to scope the import to
        :return: None
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
        Initialize the session variables found in the config. Commonly used in `app.before_request`.

        :raw-html:`<br />`

        .. code-block::

            @app.before_request
            def before_request():
                imp.init_session()

        :raw-html:`<br />`

        -----

        :return: None
        """
        if self.config.get("SESSION"):
            for key, value in self.config.get("SESSION", {}).items():
                if key not in session:
                    session[key] = value

    def import_blueprint(self, blueprint: str) -> None:
        """
        Imports the specified Flask-Imp Blueprint or a standard Flask Blueprint.

        :raw-html:`<br />`

        **Must be setup in a Python package**

        :raw-html:`<br />`

        **Example of a Flask-Imp Blueprint:**

        :raw-html:`<br />`

        Will look for a config.toml file in the blueprint folder.

        :raw-html:`<br />`

        --- Folder structure ---
        .. code-block:: text

            app
            ├── my_blueprint
            │   ├── routes
            │   │   └── index.py
            │   ├── static
            │   │   └── css
            │   │       └── style.css
            │   ├── templates
            │   │   └── my_blueprint
            │   │       └── index.html
            │   ├── __init__.py
            │   └── config.toml
            └── ...

        :raw-html:`<br />`

        --- __init__.py ---

        .. code-block::

            from flask_imp import Blueprint

            bp = Blueprint(__name__)

            bp.import_resources("routes")


            @bp.before_app_request
            def before_app_request():
                bp.init_session()


        :raw-html:`<br />`

        --- config.toml ---

        .. code-block::

            enabled = "yes"

            [settings]
            url_prefix = "/my-blueprint"
            #subdomain = ""
            #url_defaults = { }
            #static_folder = "static"
            #template_folder = "templates"
            #static_url_path = "/my-blueprint/static"
            #root_path = ""
            #cli_group = ""

            [session]
            session_values_used_by_blueprint = "will be set by bp.init_session()"

        :raw-html:`<br />`

        **Example of a standard Flask Blueprint:**

        :raw-html:`<br />`

        --- Folder structure ---

        .. code-block:: text

            app
            ├── my_blueprint
            │   ├── ...
            │   └── __init__.py
            └── ...

        :raw-html:`<br />`

        --- __init__.py ---

        .. code-block::

            from flask import Blueprint

            bp = Blueprint("my_blueprint", __name__, url_prefix="/my-blueprint")


            @bp.route("/")
            def index():
                return "regular_blueprint"

        :raw-html:`<br />`

        -----

        :param blueprint: The blueprint (folder name) to import. Must be relative.
        :return: None
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

        :raw-html:`<br />`

        **Example folder structure:**

        :raw-html:`<br />`

        .. code-block:: text

            app
            ├── blueprints
            │   ├── regular_blueprint
            │   │   ├── ...
            │   │   └── __init__.py
            │   └── flask_imp_blueprint
            │       ├── ...
            │       ├── config.toml
            │       └── __init__.py
            └── ...
            
        :raw-html:`<br />`
        
        See: `import_blueprint` for more information.

        :raw-html:`<br />`

        -----

        :param folder: The folder to import from. Must be relative.
        """

        folder_path = Path(self._app_path / folder)

        for potential_bp in folder_path.iterdir():
            self.import_blueprint(potential_bp.as_posix())

    def import_models(
            self,
            file_or_folder: str
    ) -> None:
        """
        Imports all the models from the given file or folder.


        :raw-html:`<br />`

        **Each model found will be added to the model registry.**

        See: `Imp.model()` for more information.

        :raw-html:`<br />`

        **Example usage from files:**

        :raw-html:`<br />`

        .. code-block::

            imp.import_models("users.py")
            imp.import_models("cars.py")


        :raw-html:`<br />`

        -- Folder structure --

        .. code-block::

            app
            ├── ...
            ├── users.py
            ├── cars.py
            ├── default.config.toml
            └── __init__.py

        :raw-html:`<br />`

        **Example usage from folders:**

        :raw-html:`<br />`

        .. code-block::

            imp.import_models("models")

        :raw-html:`<br />`

        -- Folder structure --

        .. code-block::

            app
            ├── ...
            ├── models
            │   ├── users.py
            │   └── cars.py
            ├── default.config.toml
            └── __init__.py

        :raw-html:`<br />`

        **Example of model file:**

        :raw-html:`<br />`

        -- users.py --

        .. code-block::

            from app.extensions import db

            class User(db.Model):
                attribute = db.Column(db.String(255))

        :raw-html:`<br />`

        -----

        :param file_or_folder: The file or folder to import from. Must be relative.
        :return: None
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
        Returns the model class for the given ORM class name.

        :raw-html:`<br />`

        This is used to omit the need to import the models from their locations.

        :raw-html:`<br />`

        **For example, this:**

        :raw-html:`<br />`

        .. code-block::

            from app.models.user import User
            from app.models.cars import Cars

        :raw-html:`<br />`

        **Can be replaced with:**

        :raw-html:`<br />`

        .. code-block::

            from app.extensions import imp

            User = imp.model("User")
            Cars = imp.model("Cars")

        :raw-html:`<br />`

        imp.model("User") -> <class 'app.models.User'>

        :raw-html:`<br />`

        Although this method is convenient, you lose out on an IDE's ability of attribute and method
        suggestions due to the type being unknown.

        :raw-html:`<br />`

        -----
        :param class_: The class name of the model to return.
        :return: The model class [DefaultMeta].
        """
        return self.__model_registry__.class_(class_)

    def model_meta(self, class_: Union[str, DefaultMeta]) -> dict:
        """
        Returns meta information for the given ORM class name

        :raw-html:`<br />`

        **Example:**

        :raw-html:`<br />`

        .. code-block::

            from app.extensions import imp

            User = imp.model("User")

            print(imp.model_meta(User))
            # or
            print(imp.model_meta("User"))

        :raw-html:`<br />`
        Will output:

        {"location": "app.models.user", "table_name": "user"}

        :raw-html:`<br />`

        **Advanced use case:**

        `location` can be used to import a function from the model file using Pythons importlib.

        :raw-html:`<br />`

        Here's an example:

        :raw-html:`<br />`

        .. code-block::

            from app.extensions import imp


            users_meta = imp.model_meta("User")
            users_module = import_module(users_meta["location"])
            users_module.some_function()

        :raw-html:`<br />`

        `table_name` is the snake_case version of the class name, pulled from `__table_name__`, which can be useful
        if you'd like to use the table name in a raw query in a route.

        :raw-html:`<br />`

        -----

        :param class_: The class name of the model to return [Class Instance | Name of class as String].
        :return: dict of meta-information.
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
