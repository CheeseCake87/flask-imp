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

    def __init__(self, dunder_name: str, config: ImpBlueprintConfig) -> None:
        """
        Initializes the ImpBlueprint.

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
            raise NoConfigProvided(f"No config was provided for {self.location}")

        self.config = config

        if not self.config.url_prefix:
            self.config.url_prefix = f"/{slug(self.bp_name)}"

        if config.database_binds:
            self._process_database_binds(config.database_binds)

        super().__init__(self.bp_name, self.package, **self.config.super_settings())

    @_prevent_if_disabled
    def _process_database_binds(
        self, database_binds: t.Optional[t.Iterable[DatabaseConfig]] = None
    ) -> None:
        """
        Processes the database binds and adds them to the blueprint.

        :param config: The blueprint's config.
        :return: None
        """
        for database_bind in database_binds:
            self._database_binds.add(
                partial(_partial_database_binds, database_bind=database_bind)
            )

    @_prevent_if_disabled
    def import_resources(self, folder: str = "routes") -> None:
        """
        Will import all the resources (cli, routes, filters, context_processors...) from the given folder.
        Given folder must be relative to the blueprint (in the same folder as the __init__.py file).

        :param folder: Folder to look for resources in. Defaults to "routes". Must be relative.
        :return: None
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

        :param folder: Folder to look for nested blueprints in.
        :return: None
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

        :param template: The template name to push the blueprint name to.
        :return: str - The template name with the blueprint name pushed to it.
        """
        return f"{self.name}/{template}"
