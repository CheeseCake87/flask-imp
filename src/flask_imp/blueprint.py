import logging
from importlib import import_module
from importlib.util import find_spec
from inspect import getmembers
from pathlib import Path
from typing import Protocol

from flask import Blueprint
from flask import session

from .helpers import _init_bp_config
from .utilities import cast_to_import_str


class Imp(Protocol):
    def import_models(
            self,
            file_or_folder: str
    ) -> None:
        ...


class ImpBlueprint(Blueprint):
    """
    A Class that extends the capabilities of the Flask Blueprint class.
    """
    enabled: bool = False
    location: Path
    bp_name: str
    package: str
    session: dict
    settings: dict

    _imp_instance: Imp

    def __init__(self, dunder_name: str, config_file: str = "config.toml"):
        """
        Creates a new ImpBlueprint instance.

        :raw-html:`<br />`

        `config.toml` must be in the same directory as the `__init__.py` file.

        :raw-html:`<br />`

        -- config.toml --
        .. code-block::

            enabled = "yes"

            [settings]
            url_prefix = ""
            subdomain = ""
            url_defaults = { }
            static_folder = ""
            template_folder = ""
            static_url_path = ""
            #root_path = ""
            #cli_group = ""

            [session]
            var = ""


        :raw-html:`<br />`

        -----

        :param dunder_name: __name__
        :param config_file: Must be in the same directory as the blueprint, defaults to "config.toml"
        """
        self.package = dunder_name
        self.app_name = dunder_name.split(".")[0]

        spec = find_spec(self.package)

        if spec is None:
            raise ImportError(f"Cannot find origin of {self.package}")

        self.location = Path(f"{spec.origin}").parent
        self.bp_name = self.location.name

        self.enabled, self.session, self.settings = _init_bp_config(self.bp_name, self.location / config_file)

        if self.enabled:
            super().__init__(
                self.bp_name,
                self.package,
                **self.settings
            )
            self._imp_instance = self._set_imp_instance()

    def _set_imp_instance(self) -> Imp:
        """
        Internal method.
        Finds the Imp instance in the app module.
        """
        from flask_imp import Imp

        app_module = import_module(self.app_name)
        for name, value in getmembers(app_module):
            if isinstance(value, Imp):
                return value

        raise ImportError(f"Cannot find Imp instance in {self.app_name}")

    def import_resources(self, folder: str = "routes") -> None:
        """
        Will import all the resources (cli, routes, filters, context_processors...) from the given folder.
        Given folder must be relative to the blueprint (in the same folder as the __init__.py file).

        :raw-html:`<br />`

        **Example use:**

        :raw-html:`<br />`

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
        if not self.enabled:
            return

        resource_path = self.location / folder
        if not resource_path.exists():
            raise NotADirectoryError(f"{resource_path} is not a directory")

        resources = resource_path.glob("*.py")
        for resource in resources:
            try:
                import_module(f"{self.package}.{folder}.{resource.stem}")
            except ImportError as e:
                raise ImportError(f"Error when importing {self.package}.{resource}: {e}")

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
        if not self.enabled:
            return

        if Path(blueprint).is_absolute():
            potential_bp = Path(blueprint)
        else:
            potential_bp = Path(self.location / blueprint)

        if potential_bp.exists() and potential_bp.is_dir():
            module = import_module(
                cast_to_import_str(self.package.split(".")[0], potential_bp)
            )
            for name, value in getmembers(module):
                if isinstance(value, Blueprint):
                    if hasattr(value, "enabled"):
                        if value.enabled:
                            self.register_blueprint(value)
                        else:
                            logging.debug(f"Blueprint {name} is disabled")

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
        if not self.enabled:
            return

        folder_path = Path(self.location / folder)

        for potential_bp in folder_path.iterdir():
            self.import_nested_blueprint(potential_bp.as_posix())

    def init_session(self) -> None:
        """
        Similar to the `Imp.init_session()` method,
        but scoped to the current blueprint's config.toml session values.

        :raw-html:`<br />`

        **Example usage:**

        :raw-html:`<br />`

        .. code-block::

            @bp.before_app_request
            def before_app_request():
                bp.init_session()

        :raw-html:`<br />`

        -----

        :return: None

        """
        if not self.enabled:
            return

        for key in self.session:
            if key not in session:
                session.update(self.session)
                break

    def import_models(
            self,
            file_or_folder: str
    ) -> None:
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
        if not self.enabled:
            return

        file_or_folder_path = Path(self.location / file_or_folder)

        self._imp_instance.import_models(file_or_folder_path.as_posix())

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
