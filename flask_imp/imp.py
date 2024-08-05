import typing as t
from importlib import import_module
from inspect import getmembers
from inspect import isclass
from pathlib import Path

from flask import Flask, Blueprint, session
from flask_sqlalchemy.model import DefaultMeta

from .config import ImpConfig
from .protocols import ImpBlueprint
from .registeries import ModelRegistry
from .utilities import cast_to_import_str, build_database_main, build_database_binds


class Imp:
    app: Flask
    app_name: str
    app_path: Path
    app_instance_path: Path
    app_folder: Path
    app_resources_imported: bool = False

    model_registry: ModelRegistry

    config: ImpConfig

    def __init__(
            self,
            app: Flask = None,
            config: ImpConfig = None,
    ) -> None:
        if app is not None:
            self.init_app(app, config)

    def init_app(
            self,
            app: Flask,
            config: ImpConfig = None,
    ) -> None:
        """
        Initializes the app with the flask-imp extension.

        :param app: The flask app to initialize.
        :param config: The config to use
        :return: None
        """

        if app is None:
            raise ImportError(
                "No app was passed in, do imp = Imp(flaskapp) or app.init_app(flaskapp)"
            )
        if not isinstance(app, Flask):
            raise TypeError("The app that was passed in is not an instance of Flask")

        if "imp" in app.extensions:
            raise ImportError("The app has already been initialized with flask-imp.")

        self.app = app
        self.app_name = app.name
        self.app_path = Path(self.app.root_path)
        self.app_instance_path = Path(self.app.instance_path)
        self.app_folder = self.app_path.parent
        self.app.extensions["imp"] = self

        self.model_registry = ModelRegistry()

        if config:
            self.config = config
        else:
            self.config = ImpConfig()
            self.config.load_config_from_flask(app)

        self._apply_sqlalchemy_config()
        self._init_session()

        self.app_instance_path.mkdir(exist_ok=True)

    def import_app_resources(
            self,
            folder: str = "resources",
            factories: t.Optional[t.List] = None,
            static_folder: str = "static",
            templates_folder: str = "templates",
            scope_import: t.Optional[t.Dict] = None,
    ) -> None:
        """
        Imports the app resources from the given folder.

        :param folder: The folder to import from, must be relative.
        :param factories: A list of function names to call with the app instance.
        :param static_folder: The name of the static folder (if not found will be set to None)
        :param templates_folder: The name of the templates folder (if not found will be set to None)
        :param scope_import: A dict of files to import e.g. {"folder_name": "*"}.
        :return: None
        """

        # Check if the app resources have already been imported
        if self.app_resources_imported:
            raise ImportError("The app resources can only be imported once.")

        self.app_resources_imported = True

        # Set defaults
        if factories is None:
            factories = []
        if scope_import is None:
            scope_import = {"*": ["*"]}

        # Build folders
        resources_folder = self.app_path / folder
        app_static_folder = resources_folder / static_folder
        app_templates_folder = resources_folder / templates_folder

        if not resources_folder.exists():
            raise ImportError(
                f"Cannot find resources collection folder at: {resources_folder}"
            )

        if not resources_folder.is_dir():
            raise ImportError(f"Resources collection must be a folder, value given: {resources_folder}")

        self.app.static_folder = (
            app_static_folder.as_posix() if app_static_folder.exists() else None
        )
        self.app.template_folder = (
            app_templates_folder.as_posix() if app_templates_folder.exists() else None
        )

        skip_folders = (
            "static",
            "templates",
        )

        for item in resources_folder.iterdir():
            if item.name.startswith("__"):
                continue

            if item.is_file() and item.suffix == ".py":
                if "*" in scope_import:
                    if "*" in scope_import["*"]:
                        self._import_resource_module(item, factories)
                    else:
                        if item.name in scope_import["*"]:
                            self._import_resource_module(item, factories)

                if "." in scope_import:
                    if "*" in scope_import["."]:
                        self._import_resource_module(item, factories)
                    else:
                        if item.name in scope_import["."]:
                            self._import_resource_module(item, factories)

            if item.is_dir():
                # skip the static and templates folders
                if item.name in skip_folders:
                    continue

                for py_file_in_item in item.glob("*.py"):
                    if "*" in scope_import:
                        if "*" in scope_import["*"]:
                            self._import_resource_module(py_file_in_item, factories)
                        else:
                            if py_file_in_item.name in scope_import["*"]:
                                self._import_resource_module(py_file_in_item, factories)

                    if item.name in scope_import:
                        if "*" in scope_import[item.name]:
                            self._import_resource_module(py_file_in_item, factories)
                        else:
                            if py_file_in_item.name in scope_import[item.name]:
                                self._import_resource_module(py_file_in_item, factories)

    def import_blueprint(self, blueprint: str) -> None:
        """
        Import a blueprint from the given package.

        :param blueprint: The blueprint (folder name) to import. Must be relative.
        :return: None
        """

        if Path(blueprint).is_absolute():
            blueprint_path = Path(blueprint)
        else:
            blueprint_path = Path(self.app_path / blueprint)

        if blueprint_path.exists() and blueprint_path.is_dir():
            module = import_module(cast_to_import_str(self.app_name, blueprint_path))
            for name, potential_blueprint in getmembers(module):
                if isinstance(potential_blueprint, Blueprint):
                    self._blueprint_registration(potential_blueprint)

    def import_blueprints(self, folder: str) -> None:
        """
        Import all blueprints from the given folder.

        :param folder: The folder to import from. Must be relative.
        :return: None
        """

        folder_path = Path(self.app_path / folder)

        if not folder_path.exists():
            raise ImportError(f"Cannot find blueprints folder at {folder_path}")

        if not folder_path.is_dir():
            raise ImportError(f"Blueprints must be a folder {folder_path}")

        for potential_bp in folder_path.iterdir():
            self.import_blueprint(f"{potential_bp}")

    def import_models(self, file_or_folder: str) -> None:
        """
        Import all models from the given file or folder.

        :param file_or_folder: The file or folder to import from. Must be relative.
        :return: None
        """

        if Path(file_or_folder).is_absolute():
            file_or_folder_path = Path(file_or_folder)
        else:
            file_or_folder_path = Path(self.app_path / file_or_folder)

        if file_or_folder_path.is_file() and file_or_folder_path.suffix == ".py":
            self._process_model(file_or_folder_path)

        elif file_or_folder_path.is_dir():
            for model_file in [
                _ for _ in file_or_folder_path.iterdir() if "__" not in _.name
            ]:
                self._process_model(model_file)

    def model(self, class_: str) -> DefaultMeta:
        """
        Returns the model class for the given ORM class name.

        :param class_: The class name of the model to return.
        :return: The model class [DefaultMeta].
        """
        return self.model_registry.class_(class_)

    def model_meta(self, class_: t.Union[str, DefaultMeta]) -> dict:
        """
        Returns meta information for the given ORM class name.

        :param class_: The class name of the model to return [Class Instance | Name of class as String].
        :return: dict of meta-information.
        """

        def check_for_table_name(model_):
            if not hasattr(model_, "__tablename__"):
                raise AttributeError(f"{model_} is not a valid model")

        if isinstance(class_, str):
            model = self.model_registry.class_(class_)
            check_for_table_name(model)
            return {
                "location": model.__module__,
                "table_name": model.__tablename__,
            }

        return {
            "location": class_.__module__,
            "table_name": class_.__tablename__,
        }

    def _apply_sqlalchemy_config(self):
        if "SQLALCHEMY_DATABASE_URI" not in self.app.config:
            build_database_main(
                self.app,
                self.app_instance_path,
                self.config.IMP_DATABASE_MAIN
            )

        if "SQLALCHEMY_BINDS" not in self.app.config:
            build_database_binds(
                self.app,
                self.app_instance_path,
                self.config.IMP_DATABASE_BINDS
            )

    def _import_resource_module(self, module: Path, factories: list):
        try:
            with self.app.app_context():
                file_module = import_module(cast_to_import_str(self.app_name, module))

                for instance_factory in factories:
                    if hasattr(file_module, instance_factory):
                        getattr(file_module, instance_factory)(self.app)

        except ImportError as e:
            raise ImportError(f"Error when importing {module}: {e}")

    def _blueprint_registration(self, blueprint: t.Union[Blueprint, ImpBlueprint]):

        if hasattr(blueprint, "config"):
            if blueprint.config.enabled:

                if hasattr(blueprint, "_models"):
                    for partial_model in blueprint._models:  # noqa
                        partial_model(imp_instance=self)

                if hasattr(blueprint, "_database_binds"):
                    for partial_database_bind in blueprint._database_binds:  # noqa
                        partial_database_bind(imp_instance=self)

                if hasattr(blueprint, "_nested_blueprints"):
                    for nested_blueprint in blueprint._nested_blueprints:  # noqa
                        self._nested_blueprint_registration(blueprint, nested_blueprint)

                if hasattr(blueprint, "init_session"):
                    if blueprint.init_session:
                        self.config.IMP_INIT_SESSION.update(blueprint.init_session)

                self.app.register_blueprint(blueprint)

                return

            else:

                self.app.logger.debug(f"Imp Blueprint [{blueprint.name}] is disabled.")

        else:

            self.app.register_blueprint(blueprint)

    def _nested_blueprint_registration(
            self,
            parent: t.Union[Blueprint, ImpBlueprint],
            child: t.Union[Blueprint, ImpBlueprint],
    ):

        if hasattr(parent, "config"):
            if not parent.config.enabled:
                return

        if hasattr(child, "config"):
            if child.config.enabled:
                parent.register_blueprint(child)  # noqa

                if hasattr(child, "_models"):
                    for partial_model in child._models:  # noqa
                        partial_model(imp_instance=self)

                if hasattr(child, "_database_binds"):
                    for partial_database_bind in child._database_binds:  # noqa
                        partial_database_bind(imp_instance=self)

                if hasattr(child, "init_session"):
                    if child.init_session:
                        self.config.IMP_INIT_SESSION.update(child.init_session)

                return

            else:

                self.app.logger.debug(f"Imp Blueprint [{child.name}] is disabled. Parent: [{parent.name}]")

        else:

            parent.register_blueprint(child)

    def _process_model(self, path: Path):
        """
        Picks apart the model from_file and builds a registry of the models found.
        """
        import_string = cast_to_import_str(self.app_name, path)
        try:
            model_module = import_module(import_string)
            for name, value in getmembers(model_module, isclass):
                if hasattr(value, "__tablename__"):
                    self.model_registry.add(name, value)

        except ImportError as e:
            raise ImportError(f"Error when importing {import_string}: {e}")

    def _init_session(self) -> None:
        """
        :return: None
        """
        if self.config.IMP_INIT_SESSION:
            @self.app.before_request
            def imp_before_request():
                session.update(
                    {k: v for k, v in self.config.IMP_INIT_SESSION.items() if k not in session}
                )
