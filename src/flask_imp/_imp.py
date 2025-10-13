import typing as t
from importlib import import_module
from inspect import getmembers
from inspect import isclass
from pathlib import Path

from flask import Flask, Blueprint, session
from flask_sqlalchemy.model import DefaultMeta

from ._imp_blueprint import ImpBlueprint
from ._registries import ModelRegistry
from ._utilities import cast_to_import_str, build_database_main, build_database_binds
from .config import ImpConfig


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
        app: t.Optional[Flask] = None,
        config: t.Optional[ImpConfig] = None,
    ) -> None:
        if app is not None:
            self.init_app(app, config)

    def init_app(
        self,
        app: Flask,
        config: t.Optional[ImpConfig] = None,
    ) -> None:
        """
        Initializes the app with the flask-imp extension.

        :param app: the flask app to initialize
        :param config: the ImpConfig to use
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

        self._apply_sqlalchemy_config()
        self._init_session()

        self.app_instance_path.mkdir(exist_ok=True)

    def import_resources(
        self,
        folder: str = "resources",
        factories: t.Optional[t.List[str]] = None,
        scope_import: t.Optional[
            t.Dict[str, t.Union[t.List[t.Optional[str]], t.Optional[str]]]
        ] = None,
    ) -> None:
        """
        Imports app resources from the given folder. Sub folders at one level deep are supported.

        :param folder: the folder to import from, must be relative
        :param factories: a list of function names to call with the app instance, defaults to ["include"]
        :param scope_import: a dict of files to import e.g. {"folder_name": "*"}
        :return: None
        """

        # Set defaults
        if factories is None:
            factories = ["include"]
        if scope_import is None:
            scope_import = {"*": ["*"]}

        # Build folders
        resources_folder = self.app_path / folder

        if not resources_folder.exists():
            raise ImportError(f"Cannot find resources location at: {resources_folder}")

        if not resources_folder.is_dir():
            raise ImportError(
                f"Resources location must be a folder, value given: {resources_folder}"
            )

        for item in resources_folder.iterdir():
            if item.name.startswith("__"):
                continue

            if item.is_file() and item.suffix == ".py":
                # found module
                self._handle_module_import(item, factories, scope_import)

            if item.is_dir():
                # found dir
                for py_file_in_item in item.glob("*.py"):
                    # loop over dir
                    if "*" in scope_import:
                        self._handle_module_import(
                            py_file_in_item, factories, scope_import
                        )
                        continue

                    if item in scope_import:
                        self._handle_module_import(
                            py_file_in_item, factories, scope_import
                        )

    def register_imp_blueprint(self, imp_blueprint: ImpBlueprint) -> None:
        """
        Manually register a ImpBlueprint.

        :param imp_blueprint: the manually imported ImpBlueprint
        """
        self._imp_blueprint_registration(imp_blueprint)

    def import_blueprint(self, blueprint: str, package: t.Optional[str] = None) -> None:
        """
        Import a blueprint from the given package.

        :param blueprint: the blueprint (folder name) to import.
        :param package: the relative package to import from.
        """

        if Path(blueprint).is_absolute():
            blueprint_path = Path(blueprint)
        else:
            blueprint_path = Path(self.app_path / blueprint)

        if blueprint_path.exists() and blueprint_path.is_dir():
            module = import_module(
                cast_to_import_str(
                    package if package else self.app_name, blueprint_path
                )
            )
            for name, potential_blueprint in getmembers(module):
                if isinstance(potential_blueprint, ImpBlueprint):
                    self._imp_blueprint_registration(potential_blueprint)
                    continue

                if isinstance(potential_blueprint, Blueprint):
                    self._flask_blueprint_registration(potential_blueprint)

    def import_blueprints(self, folder: str, package: t.Optional[str] = None) -> None:
        """
        Import all blueprints from the given folder.

        :param folder: The folder to import from. Must be relative
        :param package: the relative package to import from.
        """

        folder_path = Path(self.app_path / folder)

        if not folder_path.exists():
            raise ImportError(f"Cannot find blueprints folder at {folder_path}")

        if not folder_path.is_dir():
            raise ImportError(f"Blueprints must be a folder {folder_path}")

        for potential_bp in folder_path.iterdir():
            self.import_blueprint(f"{potential_bp}", package)

    def import_models(self, file_or_folder: str) -> None:
        """
        Import all models from the given file or folder.

        :param file_or_folder: The file or folder to import from. Must be relative
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

    def model(self, class_: str) -> t.Union[DefaultMeta, t.Any]:
        """
        Returns the model class for the given ORM class name.

        :param class_: The class name of the model to return
        :return: The model class [DefaultMeta]
        """
        return self.model_registry.class_(class_)

    def model_meta(self, class_: t.Union[str, DefaultMeta]) -> t.Dict[str, t.Any]:
        """
        Returns meta information for the given ORM class name.

        :param class_: the class name of the model to return [Class Instance | Name of class as String]
        :return: dict of meta-information
        """

        def check_for_table_name(model_: DefaultMeta) -> None:
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

    def _apply_sqlalchemy_config(self) -> None:
        if "SQLALCHEMY_DATABASE_URI" not in self.app.config:
            build_database_main(
                self.app, self.app_instance_path, self.config.IMP_DATABASE_MAIN
            )

        if "SQLALCHEMY_BINDS" not in self.app.config:
            build_database_binds(
                flask_app=self.app,
                app_instance_path=self.app_instance_path,
                database_binds=self.config.IMP_DATABASE_BINDS
                if self.config.IMP_DATABASE_BINDS
                else None,
            )

    def _handle_module_import(
        self,
        module: Path,
        factories: list[str],
        scope_import: t.Dict[str, t.Union[t.List[str], str]],
    ) -> None:
        if module.is_dir():
            # skip if module is a folder
            return

        if "*" in scope_import:
            # import from all FOLDERS set
            if "*" in scope_import["*"]:
                # import from all FILES set, disregard name
                self._import_resource_module(module, factories)
            else:
                if module.name in scope_import["*"]:
                    # import all FILES NOT set, check if name in import
                    self._import_resource_module(module, factories)

        if "." in scope_import:
            # Import from root of folder
            if "*" in scope_import["."]:
                # import from all FILES set, disregard name
                self._import_resource_module(module, factories)
            else:
                # import all FILES NOT set, check if name in import
                if module.name in scope_import["."]:
                    self._import_resource_module(module, factories)

    def _import_resource_module(self, module: Path, factories: t.List[str]) -> None:
        try:
            with self.app.app_context():
                file_module = import_module(cast_to_import_str(self.app_name, module))
        except ImportError as e:
            raise ImportError(f"Error when importing {module}: {e}")

        for instance_factory in factories:
            if hasattr(file_module, instance_factory):
                getattr(file_module, instance_factory)(self.app)

    def _imp_blueprint_registration(self, imp_blueprint: ImpBlueprint) -> None:
        if not imp_blueprint.config.enabled:
            self.app.logger.debug(
                f"Imp Blueprint [{imp_blueprint.bp_name}] is disabled."
            )
            return

        for partial_model in imp_blueprint.models:  # noqa
            partial_model(imp_instance=self)

        for partial_database_bind in imp_blueprint.database_binds:
            partial_database_bind(imp_instance=self)

        for nested_blueprint in imp_blueprint.nested_blueprints:
            if isinstance(nested_blueprint, ImpBlueprint):
                self._nested_imp_blueprint_registration(imp_blueprint, nested_blueprint)

            elif isinstance(nested_blueprint, Blueprint):
                self._nested_flask_blueprint_registration(
                    nested_blueprint, nested_blueprint
                )

        if imp_blueprint.config.init_session:
            self.config.IMP_INIT_SESSION.update(
                imp_blueprint.config.init_session
            ) if isinstance(self.config.IMP_INIT_SESSION, dict) else None

        self._flask_blueprint_registration(imp_blueprint)

    def _nested_imp_blueprint_registration(
        self,
        parent: ImpBlueprint,
        child: ImpBlueprint,
    ) -> None:
        if not parent.config.enabled:
            return

        if not child.config.enabled:
            self.app.logger.debug(
                f"Imp Blueprint [{child.bp_name}] is disabled. Parent: [{parent.bp_name}]"
            )
            return

        parent.register_blueprint(child)

        for partial_model in child.models:
            partial_model(imp_instance=self)

        for partial_database_bind in child.database_binds:  # noqa
            partial_database_bind(imp_instance=self)

        if child.config.init_session:
            if self.config.IMP_INIT_SESSION is None:
                self.config.IMP_INIT_SESSION = {}

            self.config.IMP_INIT_SESSION.update(child.config.init_session)

    def _flask_blueprint_registration(self, blueprint: Blueprint) -> None:
        self.app.register_blueprint(blueprint)

    @staticmethod
    def _nested_flask_blueprint_registration(
        parent: Blueprint,
        child: Blueprint,
    ) -> None:
        parent.register_blueprint(blueprint=child)

    def _process_model(self, path: Path) -> None:
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
        if isinstance(self.config.IMP_INIT_SESSION, dict):
            _: t.Dict[str, t.Any] = self.config.IMP_INIT_SESSION

            @self.app.before_request
            def imp_before_request() -> None:
                session.update({k: v for k, v in _.items() if k not in session})
