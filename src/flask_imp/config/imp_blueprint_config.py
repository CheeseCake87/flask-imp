import typing as t
from dataclasses import dataclass


@dataclass
class ImpBlueprintConfig:
    from .database_config import DatabaseConfig

    enabled: t.Optional[bool] = None
    url_prefix: t.Optional[str] = None
    subdomain: t.Optional[str] = None
    url_default: t.Optional[t.Dict[str, t.Any]] = None
    static_folder: t.Optional[str] = None
    template_folder: t.Optional[str] = None
    static_url_path: t.Optional[str] = None
    root_path: t.Optional[str] = None
    cli_group: t.Optional[str] = None

    init_session: t.Optional[t.Dict[str, t.Any]] = None

    database_binds: t.Optional[t.Iterable[DatabaseConfig]] = None

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
        enabled: bool = False,
        url_prefix: t.Optional[str] = None,
        subdomain: t.Optional[str] = None,
        url_defaults: t.Optional[t.Dict[str, t.Any]] = None,
        static_folder: t.Optional[str] = None,
        template_folder: t.Optional[str] = None,
        static_url_path: t.Optional[str] = None,
        root_path: t.Optional[str] = None,
        cli_group: t.Optional[str] = None,
        init_session: t.Optional[t.Dict[str, t.Any]] = None,
        database_binds: t.Optional[t.Iterable[DatabaseConfig]] = None,
    ):
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
