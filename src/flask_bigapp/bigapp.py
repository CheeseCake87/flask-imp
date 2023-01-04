import logging
import os
import re
from importlib import import_module
from inspect import getmembers
from inspect import isclass
from pathlib import Path
from types import ModuleType
from typing import Dict, TextIO, Union, Optional, Any

from flask import Blueprint
from flask import Flask
from flask import session
from flask_sqlalchemy.model import DefaultMeta
from toml import load as toml_load

from .blueprint import BigAppBlueprint
from .resources import Resources
from .utilities import cast_to_bool, cast_to_import_str, deprecated


class _ModelRegistry:
    registry: Dict[str, Any]

    def __init__(self):
        self.registry = dict()

    def assert_exists(self, ref: str):
        if ref not in self.registry:
            raise KeyError(
                f"Model {ref} not found in model registry \n"
                f"Available models: {', '.join(self.registry.keys())}"
            )

    def get(self, ref: str) -> dict:
        self.assert_exists(ref)
        return self.registry[ref]

    def class_(self, ref: str) -> DefaultMeta:
        self.assert_exists(ref)
        return self.registry[ref]['class']

    def add(self, ref, model: Optional[ModuleType] = None):
        self.registry[ref] = {
            'ref': ref,
            'class': model
        }

    def __repr__(self):
        return f"ModelRegistry({self.registry})"


class BigApp(object):
    session: Dict
    themes: Dict[str, Path]

    __blueprint_registry__: Dict[str, Optional[ModuleType]]
    __model_registry__: _ModelRegistry

    _app: Flask
    _app_name: str
    _app_path: Path
    _app_folder: Path

    _default_config: Optional[str]

    def __init__(
            self,
            app: Optional[Flask] = None,
            app_config_file: Optional[str] = None
    ) -> None:

        if app is not None:
            self.init_app(app, app_config_file)

    def init_app(
            self,
            app: Flask,
            app_config_file: Optional[str] = os.environ.get("BA_CONFIG")
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

        self.session = dict()
        self.themes = dict()
        self.__model_registry__ = _ModelRegistry()

        self._app = app
        self._app_name = app.name
        self._app_path = Path(self._app.root_path)
        self._app_folder = self._app_path.parent

        if app_config_file is None:
            app_config_file = "default.config.toml"

        self._init_config(self._app_path / app_config_file)

        self.__blueprint_registry__ = dict()

    def init_session(self) -> None:
        """
        Initialize the session variables found in the config from_file.
        Use this method in the before_request route.
        """
        for key in self.session:
            if key not in session:
                session.update(self.session)
                break

    def import_builtins(self, folder: Union[str, Path] = "builtins") -> None:
        """
        Folder must be relative ( from_folder="here" not from_folder="/home/user/app/from_folder" )
        """
        if isinstance(folder, str):
            builtins_folder = Path(self._app_path / folder)
        else:
            builtins_folder = folder

        if builtins_folder.is_dir():
            with self._app.app_context():
                for py_file in builtins_folder.glob("*.py"):
                    module = import_module(
                        f"{cast_to_import_str(self._app_name, builtins_folder)}.{py_file.stem}")
                    if hasattr(module, "loader"):
                        module.loader(self._app)

    def import_blueprints(self, folder: str) -> None:
        """
        Imports all the blueprints in the given from_folder.

        Folder must be relative ( from_folder="here" not from_folder="/home/user/app/from_folder" )
        """

        folder_path = Path(self._app_path / folder)

        for potential_bp in folder_path.iterdir():
            self.import_blueprint(potential_bp)

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
            if potential_bp.name in self.__blueprint_registry__:
                raise ImportError(
                    f"Blueprint {potential_bp.name} is already registered, blueprint folders must be unique\n"
                    f"Importing from {potential_bp}"
                )
            try:
                module = import_module(
                    cast_to_import_str(self._app_name, potential_bp))
                for dir_item in dir(module):
                    _ = getattr(module, dir_item)
                    if isinstance(_, BigAppBlueprint):
                        if _.enabled:
                            self.__blueprint_registry__.update(
                                {potential_bp.name: module}
                            )
                            self._app.register_blueprint(_)
                        break
            except Exception as e:
                logging.critical(f"{e}",
                                 f"Error importing blueprint: from {potential_bp}")

    @deprecated(
        "import_structures() will be removed, Use import_themes() instead")
    def import_structures(self, structures_folder: str) -> None:
        self.import_themes(structures_folder)

    def import_themes(self, themes_folder: str) -> None:
        """
        Folder must be relative ( from_folder="here" not from_folder="/home/user/app/from_folder" )
        """
        folder_path = Path(self._app_path / themes_folder)
        for theme in folder_path.iterdir():
            self.import_theme(theme)

    def import_theme(self, theme_folder: Union[str, Path]):
        """
        Folder must be relative ( from_folder="here" not from_folder="/home/user/app/from_folder" )
        """
        if isinstance(theme_folder, str):
            theme = Path(self._app_path / theme_folder)
        else:
            theme = theme_folder

        if theme.is_dir():
            if theme.name in self.themes:
                raise ImportError(
                    f"Theme {theme.name} is already registered, theme folders must be unique\n"
                    f"Importing from {theme}"
                )

            static_folder = Path(theme / "static")
            template_folder = Path(theme / "templates")
            nested_template_folder = Path(theme / "templates" / theme.name)
            builtins_folder = Path(theme / "builtins")

            config = Path(theme / "config.toml")

            if not static_folder.exists():
                logging.debug(
                    f"Static from_folder for {theme.name} was not found, skipping")

            if not template_folder.exists():
                raise NotADirectoryError(
                    f"Template from_folder for {theme.name} was not found")

            if not nested_template_folder.exists():
                raise NotADirectoryError(
                    f"Nested template from_folder for {theme.name} was not found, \nshould look like: {nested_template_folder}")

            if not config.exists():
                logging.debug(
                    f"Config from_file for {theme.name} was not found, creating default")
                config.write_text(Resources.default_theme_config.format(
                    static_url_path=f"/{theme.name}/static"))

            loaded_config = toml_load(config)

            theme_bp = Blueprint(
                name=theme.name,
                import_name=f"{theme.name}",
                static_folder=f"{theme.absolute()}/static",
                template_folder=f"{theme.absolute()}/templates",
                static_url_path=f"{loaded_config.get('static_url_path', f'/{theme.name}/static')}",
            )

            if cast_to_bool(loaded_config.get("enabled")):

                if builtins_folder.exists():
                    self.import_builtins(builtins_folder)

                self._app.register_blueprint(theme_bp)
                self.themes.update({theme.name: theme.absolute()})

    def import_models(
            self,
            from_file: Optional[str] = None,
            from_folder: Optional[str] = None,
    ) -> None:
        """
        Imports model files from a single from_file or a from_folder. Both are allowed to be set.

        File and Folder must be relative ( from_folder="here" not from_folder="/home/user/app/from_folder" )
        """

        def model_processor(path: Path):
            """
            Picks apart the model from_file and builds a registry of the models found.
            """
            import_string = cast_to_import_str(self._app_name, path).rstrip(
                ".py")
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
                logging.critical("Error importing model: ", e,
                                 f" {import_string}")

        if from_file is None and from_folder is None:
            raise ImportError(
                "No model from_file or from_folder was passed in")

        if from_folder is not None:
            folder_path = Path(self._app_path / from_folder)
            if folder_path.is_dir():
                for model_file in folder_path.glob("*.py"):
                    model_processor(model_file)

        if from_file is not None:
            file_path = Path(self._app_path / from_file)
            if file_path.is_file() and file_path.suffix == ".py":
                model_processor(file_path)

    @deprecated("model_class() will be removed, Use model() instead")
    def model_class(self, class_name: str) -> Any:
        return self.model(class_name)

    def model(self, class_: str) -> DefaultMeta:
        """
        Returns the model class for the given class name
        """
        return self.__model_registry__.class_(class_)

    def model_meta(self, class_: Union[str, Any]) -> dict:
        """
        Returns the model class for the given class name
        """

        def check_for_table_name(model_):
            if not hasattr(model_, "__tablename__"):
                raise AttributeError(f"{model_} is not a valid model")

        if isinstance(class_, str):
            model = self.__model_registry__.get(class_)
            check_for_table_name(model['class'])
            return {
                "ref": model['ref'],
                "location": model['class'].__module__,
                "table_name": model['class'].__tablename__,
            }

        check_for_table_name(class_)
        return {
            "ref": class_.__name__,
            "location": class_.__module__,
            "table_name": class_.__tablename__,
        }

    def _init_config(self, config_file_path: Path):
        """
        Processes the values from the configuration from_file.
        """
        if not config_file_path.exists():
            logging.critical(
                f"Config from_file {config_file_path.name} was not found, creating default.config.toml to use")
            config_file_path.write_text(Resources.default_config.format(
                secret_key=os.urandom(24).hex()))

        config_suffix = ('.toml', '.tml')

        if config_file_path.suffix not in config_suffix:
            raise TypeError(
                f"Config from_file must be one of the following types: {config_suffix}")

        def if_env_replace(env_value: Optional[Any]) -> Any:
            """
            Looks for the replacement pattern to swap out values in the config from_file with environment variables.
            """
            pattern = re.compile(r'<(.*?)>')

            if isinstance(env_value, str):
                if re.match(pattern, env_value):
                    env_var = re.findall(pattern, env_value)[0]
                    return os.environ.get(env_var, "ENV_KEY_NOT_FOUND")
            return env_value

        def build_database_uri(block: dict) -> str:
            """
            Puts together the correct database URI depending on the type specified.

            Fails if type is not supported.
            """
            db_type = if_env_replace(block.get("type", "None"))
            db_name = if_env_replace(block.get('database_name', 'database'))

            db_location = if_env_replace(block.get("location", "db"))
            db_port = if_env_replace(str(block.get('port', 'None')))

            db_username = if_env_replace(block.get('username', 'None'))
            db_password = if_env_replace(block.get('password', 'None'))

            db_allowed = ('postgresql', 'mysql', 'oracle')

            if db_type == "sqlite":
                if db_location is not None:

                    if db_location.startswith("/"):
                        return f"sqlite:///{db_location}/{db_name}"

                    complete_path = Path(self._app_path / db_location)
                    complete_path.mkdir(parents=True, exist_ok=True)

                    return f"{db_type}:////{complete_path}/{db_name}.db"

                return f"{db_type}:////{self._app_path}/{db_name}.db"

            if db_type in db_allowed:
                return f"{db_type}://{db_username}:{db_password}@{db_location}:{db_port}/{db_name}"

            raise ValueError(
                f"Unknown database type: {db_type}, must be: postgresql / mysql / oracle / sqlite")

        config = toml_load(config_file_path)

        flask_config = config.get("flask")
        session_config = config.get("session")
        database_config = config.get("database")

        if flask_config is not None and isinstance(flask_config, dict):
            if flask_config.get("static_folder", False):
                self._app.static_folder = if_env_replace(
                    flask_config.get("static_folder"))
                del flask_config['static_folder']

            if flask_config.get("template_folder", False):
                self._app.template_folder = if_env_replace(
                    flask_config.get("template_folder"))
                del flask_config['template_folder']

            for flask_config_key, flask_config_value in flask_config.items():
                self._app.config.update({
                    str(flask_config_key).upper(): if_env_replace(
                        flask_config_value)})

        if session_config is not None and isinstance(session_config, dict):
            self.session = session_config

        if database_config is not None and isinstance(database_config, dict):
            self._app.config['SQLALCHEMY_BINDS'] = dict()
            for database_config_key, database_config_value in database_config.items():
                if database_config_value.get("enabled", False):
                    if database_config_key == "main":
                        self._app.config[
                            'SQLALCHEMY_DATABASE_URI'] = f"{build_database_uri(database_config_value)}"
                        continue

                    self._app.config['SQLALCHEMY_BINDS'].update(
                        {
                            database_config_key: f"{build_database_uri(database_config_value)}"}
                    )

    @staticmethod
    def structure_tmpl(structure: str, template: Union[str, TextIO]) -> str:
        """
        pushes together a structure name to a template location.
        """
        return f"{structure}/{template}"
