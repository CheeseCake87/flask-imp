from __future__ import annotations

import typing as t
from functools import partial
from importlib import import_module
from importlib.util import find_spec
from inspect import getmembers
from pathlib import Path

from flask import Blueprint

from ._exceptions import NoConfigProvided
from ._utilities import (
    cast_to_import_str,
    slug,
    partial_models_import,
    partial_database_binds,
)

if t.TYPE_CHECKING:
    from .config import DatabaseConfig
    from .config import SQLiteDatabaseConfig
    from .config import SQLDatabaseConfig
    from .config import ImpBlueprintConfig


class ImpBlueprint(Blueprint):
    """
    A Class that extends the capabilities of the Flask Blueprint class.
    """

    config: ImpBlueprintConfig

    location: Path
    bp_name: str
    package: str

    models: t.Set[t.Any]
    nested_blueprints: t.Set[t.Union["ImpBlueprint", Blueprint]]
    database_binds: t.Set[t.Any]

    def __init__(self, dunder_name: str, config: ImpBlueprintConfig) -> None:
        """
        Initializes the ImpBlueprint.

        :param dunder_name: __name__
        :param config: the blueprint's config.
        """

        self.models = set()
        self.database_binds = set()
        self.nested_blueprints = set()

        self.package = dunder_name

        spec = find_spec(self.package)
        if spec is None:
            raise ImportError(f"Cannot find origin of {self.package}")

        self.location = Path(f"{spec.origin}").parent
        self.bp_name = self.location.name

        if config is None:
            raise NoConfigProvided(f"No config was provided for {self.location}")

        self.config = config

        if not self.config.url_prefix:
            self.config.url_prefix = f"/{slug(self.bp_name)}"

        if config.database_binds:
            self._process_database_binds(config.database_binds)

        super().__init__(
            self.bp_name, self.package, **self.config.flask_blueprint_args()
        )

    def _prevent_if_disabled(self: "ImpBlueprint") -> bool:
        """
        A helper function that will prevent the blueprint from
        doing anything if it is disabled.
        """
        if not self.config.enabled:
            return True
        return False

    def _process_database_binds(
        self,
        database_binds: t.Optional[
            t.Iterable[t.Union[DatabaseConfig, SQLDatabaseConfig, SQLiteDatabaseConfig]]
        ],
    ) -> None:
        """
        Processes any database binds and add them to the blueprint.

        :param database_binds: the database binds to process.
        :return: None
        """
        if self._prevent_if_disabled():
            return

        if database_binds:
            for database_bind in database_binds:
                self.database_binds.add(
                    partial(partial_database_binds, database_bind=database_bind)
                )

    def as_flask_blueprint(self) -> Blueprint:
        """
        Returns the blueprint as a Flask Blueprint.

        :return: Blueprint
        """
        return Blueprint(
            self.bp_name,
            self.package,
            static_folder=self.config.static_folder,
            static_url_path=self.config.static_url_path,
            template_folder=self.config.template_folder,
            url_prefix=self.config.url_prefix,
            subdomain=self.config.subdomain,
            url_defaults=self.config.url_defaults,
            root_path=self.config.root_path,
            cli_group=self.config.cli_group,
        )

    def import_resources(self, folder: str = "routes") -> None:
        """
        Will import all the resources (cli, routes, filters, context_processors...) from the given folder.
        Given folder must be relative to the blueprint (in the same folder as the __init__.py file).

        :param folder: the folder to look for resources in. Defaults to "routes". Must be relative
        """

        if self._prevent_if_disabled():
            return

        resource_path = self.location / folder
        if not resource_path.exists():
            raise NotADirectoryError(f"{resource_path} is not a directory")

        resources = resource_path.glob("*.py")
        for resource in resources:
            try:
                import_module(f"{self.package}.{folder}.{resource.stem}")
            except ImportError as e:
                raise ImportError(
                    f"Error when importing {self.package}.{resource.stem}: {e}"
                )

    def import_nested_blueprint(self, blueprint: t.Union[str, Path]) -> None:
        """
        Imports the specified Flask-Imp Blueprint or a standard Flask Blueprint as a nested blueprint,
        under the current blueprint.

        :param blueprint: the blueprint (folder name) to import. Must be relative
        """

        if self._prevent_if_disabled():
            return

        if isinstance(blueprint, Path):
            potential_bp = blueprint
        else:
            if isinstance(blueprint, str):
                if Path(blueprint).is_absolute():
                    potential_bp = Path(blueprint)
                else:
                    potential_bp = Path(self.location / blueprint)
            else:
                raise ValueError("Blueprint must be a string or a Path object")

        if potential_bp.exists() and potential_bp.is_dir():
            module = import_module(
                cast_to_import_str(self.package.split(".")[0], potential_bp)
            )
            for name, potential in getmembers(module):
                if isinstance(potential, ImpBlueprint):
                    self.nested_blueprints.add(potential)
                    continue

                if isinstance(potential, Blueprint):
                    self.nested_blueprints.add(potential)

    def import_nested_blueprints(self, folder: str) -> None:
        """
        Imports all blueprints in the given folder.

        :param folder: the folder to look for nested blueprints in.
        """

        if self._prevent_if_disabled():
            return

        folder_path = Path(self.location / folder)

        if not folder_path.exists() or not folder_path.is_dir():
            raise NotADirectoryError(f"{folder_path} is not a directory")

        for potential_bp in folder_path.iterdir():
            self.import_nested_blueprint(blueprint=potential_bp)

    def import_models(self, file_or_folder: str) -> None:
        """
        Same actions as `Imp.import_models()`, but scoped to the current blueprint's package.

        :param file_or_folder: the file or folder to import from. Must be relative
        """

        if self._prevent_if_disabled():
            return

        self.models.add(
            partial(
                partial_models_import,
                location=self.location,
                file_or_folder=file_or_folder,
            )
        )

    def tmpl(self, template: str) -> str:
        """
        Pushes the blueprint name to the template name.

        This is useful if you ever want to change the name of the blueprint.

        :param template: the template name to push the blueprint name to
        :return: the template name with the blueprint name pushed to it
        """
        return f"{self.name}/{template}"
