import typing as t
from functools import partial
from importlib import import_module
from importlib.util import find_spec
from inspect import getmembers
from pathlib import Path

from flask import Blueprint

from .config import DatabaseConfig
from .config import ImpBlueprintConfig
from .exceptions import NoConfigProvided
from .utilities import (
    cast_to_import_str,
    slug,
    _partial_models_import,
    _partial_database_binds,
)


def _prevent_if_disabled(func) -> t.Callable:
    def decorator(self, *args, **kwargs):
        if not self.config.enabled:
            return
        return func(self, *args, **kwargs)

    return decorator


class ImpBlueprint(Blueprint):
    """
    A Class that extends the capabilities of the Flask Blueprint class.
    """

    config: ImpBlueprintConfig

    location: Path
    bp_name: str
    package: str

    _models: t.Set = None
    _nested_blueprints: t.Union[t.Set, t.Set[t.Union["ImpBlueprint", Blueprint]]] = None

    def __init__(
            self,
            dunder_name: str,
            config: ImpBlueprintConfig
    ) -> None:
        """
        :param dunder_name: __name__
        :param config: The blueprint's config.
        """

        self._models = set()
        self._database_binds = set()
        self._nested_blueprints = set()

        self.package = dunder_name

        spec = find_spec(self.package)
        if spec is None:
            raise ImportError(f"Cannot find origin of {self.package}")

        self.location = Path(f"{spec.origin}").parent
        self.bp_name = self.location.name

        if config is None:
            raise NoConfigProvided(
                f"No config was provided for {self.location}"
            )

        self.config = config

        if not self.config.url_prefix:
            self.config.url_prefix = f"/{slug(self.bp_name)}"

        if config.database_binds:
            self._process_database_binds(config.database_binds)

        super().__init__(self.bp_name, self.package, **self.config.super_settings())

    @_prevent_if_disabled
    def _process_database_binds(self, database_binds: t.Optional[t.Iterable[DatabaseConfig]] = None) -> None:
        """
        Processes the database binds and adds them to the blueprint.

        :param config: The blueprint's config.
        :return: None
        """
        for database_bind in database_binds:
            self._database_binds.add(
                partial(
                    _partial_database_binds,
                    database_bind=database_bind
                )
            )

    @_prevent_if_disabled
    def import_resources(self, folder: str = "routes") -> None:
        """
        Will import all the resources (cli, routes, filters, context_processors...) from the given folder.
        Given folder must be relative to the blueprint (in the same folder as the __init__.py file).

        **Example use:**

        --- Folder structure ---

        .. code-block::

            my_blueprint
            ├── user_routes
            │   ├── user_dashboard.py
            │   └── user_settings.py
            ├── car_routes
            │   ├── car_dashboard.py
            │   └── car_settings.py
            ├── __init__.py
            └── config.toml

        :raw-html:`<br />`

        --- __init__.py ---

        .. code-block::

            from flask_imp import Blueprint

            bp = Blueprint(__name__)

            bp.import_resources("user_routes")
            bp.import_resources("car_routes")
            ...

        :raw-html:`<br />`

        --- user_dashboard.py ---

        .. code-block::

            from flask import render_template

            from .. import bp

            @bp.route("/user-dashboard")
            def user_dashboard():
                return render_template(bp.tmpl("user_dashboard.html"))

        :raw-html:`<br />`

        The endpoint my_blueprint.user_dashboard will be available at /my_blueprint/user-dashboard

        :raw-html:`<br />`

        -----

        :param folder: Folder to look for resources in. Defaults to "routes". Must be relative.
        """

        resource_path = self.location / folder
        if not resource_path.exists():
            raise NotADirectoryError(f"{resource_path} is not a directory")

        resources = resource_path.glob("*.py")
        for resource in resources:
            try:
                import_module(f"{self.package}.{folder}.{resource.stem}")
            except ImportError as e:
                raise ImportError(
                    f"Error when importing {self.package}.{resource}: {e}"
                )

    @_prevent_if_disabled
    def import_nested_blueprint(self, blueprint: str) -> None:
        """
        Imports the specified Flask-Imp Blueprint or a standard Flask Blueprint as a nested blueprint,
        under the current blueprint.

        :raw-html:`<br />`

        Has the same import rules as the `Imp.import_blueprint()` method.

        :raw-html:`<br />`

        **Must be setup in a Python package**

        :raw-html:`<br />`

        **Example:**

        :raw-html:`<br />`

        --- Folder structure ---
        .. code-block::

            app
            ├── my_blueprint
            │   ├── ...
            │   ├── my_nested_blueprint
            │   │   ├── ...
            │   │   ├── __init__.py
            │   │   └── config.toml
            │   ├── __init__.py
            │   └── config.toml
            └── ...

        :raw-html:`<br />`

        --- my_blueprint/__init__.py ---

        .. code-block::

            from flask_imp import Blueprint

            bp = Blueprint(__name__)

            bp.import_nested_blueprint("my_nested_blueprint")

            ...


        :raw-html:`<br />`

        -----

        :param blueprint: The blueprint (folder name) to import. Must be relative.
        :return: None
        """
        if Path(blueprint).is_absolute():
            potential_bp = Path(blueprint)
        else:
            potential_bp = Path(self.location / blueprint)

        if potential_bp.exists() and potential_bp.is_dir():
            module = import_module(
                cast_to_import_str(self.package.split(".")[0], potential_bp)
            )
            for name, potential in getmembers(module):
                if isinstance(potential, Blueprint):
                    self._nested_blueprints.add(potential)

    @_prevent_if_disabled
    def import_nested_blueprints(self, folder: str) -> None:
        """
        Imports all blueprints in the given folder.

        .. Note::
            Folder has no requirement to be a Python package.

        :raw-html:`<br />`

        See `Imp.import_nested_blueprint()` for more information.

        :raw-html:`<br />`

        **Example:**

        :raw-html:`<br />`

        --- Folder structure ---

        .. code-block::

            app
            ├── my_blueprint
            │   ├── ...
            │   ├── nested_blueprints
            │   │   ├── my_nested_blueprint_1
            │   │   │   ├── ...
            │   │   │   ├── __init__.py
            │   │   │   └── config.toml
            │   │   ├── my_nested_blueprint_2
            │   │   │   ├── ...
            │   │   │   ├── __init__.py
            │   │   │   └── config.toml
            │   │   └── my_nested_blueprint_3
            │   │       ├── ...
            │   │       ├── __init__.py
            │   │       └── config.toml
            │   ├── __init__.py
            │   └── config.toml
            └── ...

        :raw-html:`<br />`

        --- my_blueprint/__init__.py ---

        .. code-block::

            from flask_imp import Blueprint

            bp = Blueprint(__name__)
            bp.import_nested_blueprints("nested_blueprints")
            ...

        :raw-html:`<br />`

        All blueprints in the nested_blueprints folder will be imported and nested under my_blueprint.

        :raw-html:`<br />`

        -----

        :param folder: Folder to look for nested blueprints in.
        Must be relative.
        """

        folder_path = Path(self.location / folder)

        if not folder_path.exists() or not folder_path.is_dir():
            raise NotADirectoryError(f"{folder_path} is not a directory")

        for potential_bp in folder_path.iterdir():
            self.import_nested_blueprint(f"{potential_bp}")

    @_prevent_if_disabled
    def import_models(self, file_or_folder: str) -> None:
        """
        Same actions as `Imp.import_models()`, but scoped to the current blueprint's package.

        :raw-html:`<br />`

        **Each model found will be added to the model registry.**

        :raw-html:`<br />`

        See: `Imp.model()` for more information.

        :raw-html:`<br />`

        **Example usage from files:**

        :raw-html:`<br />`

        .. code-block::

            # in my_blueprint/__init__.py
            bp.import_models("users.py")
            bp.import_models("cars.py")

        :raw-html:`<br />`

        -- Folder structure --

        .. code-block::

            my_blueprint
            ├── ...
            ├── users.py
            ├── cars.py
            ├── config.toml
            └── __init__.py


        :raw-html:`<br />`

        **Example usage from folders:**

        :raw-html:`<br />`

        .. code-block::

            # in my_blueprint/__init__.py
            bp.import_models("models")

        :raw-html:`<br />`

        -- Folder structure --

        .. code-block::

            my_blueprint
            ├── ...
            ├── models
            │   ├── users.py
            │   └── cars.py
            ├── config.toml
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
        self._models.add(
            partial(
                _partial_models_import,
                location=self.location,
                file_or_folder=file_or_folder,
            )
        )

    def tmpl(self, template: str) -> str:
        """
        Pushes the blueprint name to the template name.
        This saves time in having to type out the blueprint name when rendering a
        template file from the blueprint's template folder.

        :raw-html:`<br />`

        **Example usage:**

        :raw-html:`<br />`

        .. code-block::

            @bp.route("/")
            def index():
                return render_template(bp.tmpl("index.html"))

        :raw-html:`<br />`

        -- Folder structure --

        .. code-block::

            my_blueprint
            ├── ...
            ├── templates
            │   └── my_blueprint
            │       └── index.html
            ├── config.toml
            └── __init__.py

        :raw-html:`<br />`

        bp.tmpl("index.html") will return "my_blueprint/index.html"

        :raw-html:`<br />`

        This use case is a common workaround in Flask to allow for multiple templates with the same name,
        but in different registered template folders.

        :raw-html:`<br />`

        -----

        :param template: The template name to push the blueprint name to.
        :return: str - The template name with the blueprint name pushed to it.
        """
        return f"{self.name}/{template}"
