from __future__ import annotations

import typing as t
from dataclasses import dataclass

if t.TYPE_CHECKING:
    from ._database_config import DatabaseConfig
    from ._sql_database_config import SQLDatabaseConfig
    from ._sqlite_database_config import SQLiteDatabaseConfig


@dataclass
class ImpBlueprintConfig:
    """
    Blueprint configuration class used by the ImpBlueprint class.
    """

    enabled: bool
    url_prefix: t.Optional[str] = None
    subdomain: t.Optional[str] = None
    url_default: t.Optional[t.Dict[str, t.Any]] = None
    static_folder: t.Optional[str] = None
    template_folder: t.Optional[str] = None
    static_url_path: t.Optional[str] = None
    root_path: t.Optional[str] = None
    cli_group: t.Optional[str] = None

    init_session: t.Optional[t.Dict[str, t.Any]] = None

    database_binds: t.Optional[
        t.Iterable[t.Union[DatabaseConfig, SQLDatabaseConfig, SQLiteDatabaseConfig]]
    ] = None

    _blueprint_attrs = {
        "url_prefix",
        "subdomain",
        "url_defaults",
        "static_folder",
        "template_folder",
        "static_url_path",
        "root_path",
        "cli_group",
    }

    def __init__(
        self,
        enabled: bool = True,
        url_prefix: t.Optional[str] = None,
        subdomain: t.Optional[str] = None,
        url_defaults: t.Optional[t.Dict[str, t.Any]] = None,
        static_folder: t.Optional[str] = None,
        template_folder: t.Optional[str] = None,
        static_url_path: t.Optional[str] = None,
        root_path: t.Optional[str] = None,
        cli_group: t.Optional[str] = None,
        init_session: t.Optional[t.Dict[str, t.Any]] = None,
        database_binds: t.Optional[
            t.Iterable[t.Union[DatabaseConfig, SQLDatabaseConfig, SQLiteDatabaseConfig]]
        ] = None,
    ):
        """
        Blueprint configuration class used by the ImpBlueprint class.

        This configuration is used to configure a regular Flask Blueprint with additional
        configuration options.

        :param enabled: whether the blueprint is enabled - defaults to False
        :param url_prefix: the blueprint URL prefix - defaults to None
        :param subdomain: the blueprint subdomain - defaults to None
        :param url_defaults: the blueprint URL defaults - defaults to None
        :param static_folder: the blueprint static folder - defaults to None
        :param template_folder: the blueprint template folder - defaults to None
        :param static_url_path: the blueprint static URL path - defaults to None
        :param root_path: the blueprint root path - defaults to None
        :param cli_group: the blueprint CLI group - defaults to None
        :param init_session: the blueprint initial session - defaults to None
        :param database_binds: the blueprint database binds - defaults to None
        """
        self.enabled = enabled
        self.url_prefix = url_prefix
        self.subdomain = subdomain
        self.url_defaults = url_defaults
        self.static_folder = static_folder
        self.template_folder = template_folder
        self.static_url_path = static_url_path
        self.root_path = root_path
        self.cli_group = cli_group
        self.init_session = init_session

        if database_binds is None:
            self.database_binds = []
        else:
            self.database_binds = database_binds

    def flask_blueprint_args(self) -> t.Dict[str, t.Any]:
        return {k: getattr(self, k) for k in self._blueprint_attrs if getattr(self, k)}
