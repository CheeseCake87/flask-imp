import logging
from importlib import import_module
from importlib.util import find_spec
from inspect import getmembers
from pathlib import Path
from typing import Protocol

from flask import Blueprint
from flask import session

from .helpers import init_bp_config
from .utilities import cast_to_import_str


class BigApp(Protocol):
    def import_models(
            self,
            file_or_folder: str
    ) -> None:
        ...


class BigAppBlueprint(Blueprint):
    """
    Class that extends the capabilities of the Flask Blueprint class.
    """
    enabled: bool = False
    location: Path
    bp_name: str
    package: str
    session: dict
    settings: dict

    _bigapp_instance: BigApp

    def __init__(self, dunder_name: str, config_file: str = "config.toml"):
        r"""
        :param dunder_name: Must be __name__
        :param config_file: Must be in the same directory as the blueprint, defaults to "config.toml"

        -- config.toml example:
        ::
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
        """
        self.package = dunder_name
        self.app_name = dunder_name.split(".")[0]

        spec = find_spec(self.package)

        if spec is None:
            raise ImportError(f"Cannot find origin of {self.package}")

        self.location = Path(f"{spec.origin}").parent
        self.bp_name = self.location.name

        self.enabled, self.session, self.settings = init_bp_config(self.bp_name, self.location / config_file)

        if self.enabled:
            super().__init__(
                self.bp_name,
                self.package,
                **self.settings
            )
            self._bigapp_instance = self._set_bigapp_instance()

    def _set_bigapp_instance(self) -> BigApp:
        """
        Internal method.
        Finds the BigApp instance in the app module.
        """
        from flask_bigapp import BigApp

        app_module = import_module(self.app_name)
        for name, value in getmembers(app_module):
            if isinstance(value, BigApp):
                return value

        raise ImportError(f"Cannot find BigApp instance in {self.app_name}")

    def import_resources(self, folder: str = "routes") -> None:
        """
        Imports all the resources (cli, routes, filters, context_processors...) in the given folder.

        :param folder: Folder to look for resources in.
        Defaults to "routes".
        Must be relative.
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

    def import_nested_blueprints(self, folder: str) -> None:
        """
        Imports all blueprints in the given folder.
        Nests them under the current blueprint.
        url: /current_blueprint/nested_blueprint

        :param folder: Folder to look for nested blueprints in.
        Must be relative.
        """
        if not self.enabled:
            return

        folder_path = Path(self.location / folder)

        for potential_bp in folder_path.iterdir():
            self.import_nested_blueprint(potential_bp.as_posix())

    def import_nested_blueprint(self, blueprint: str) -> None:
        """
        Imports a single nested blueprint from the given path.

        :param blueprint: Name of the blueprint (Python Package) to import.
        Must be relative.
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

    def init_session(self) -> None:
        """
        Initialize the session variables found in the config from_file.
        Use this method in the before_request route.
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
        Imports all the models in the given file or folder.

        :param file_or_folder: The file or folder to import from.
        Must be relative.
        """
        if not self.enabled:
            return

        file_or_folder_path = Path(self.location / file_or_folder)

        self._bigapp_instance.import_models(file_or_folder_path.as_posix())

    def tmpl(self, template) -> str:
        """
        Pushes together the name of the blueprint and the template from_file to look for.
        This is a small-time saving method to allow you to only type
        bp.tmpl("index.html") when looking for template files.
        """
        return f"{self.name}/{template}"
