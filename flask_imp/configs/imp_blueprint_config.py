import typing as t
from dataclasses import dataclass


@dataclass
class ImpBlueprintConfig:
    from ..protocols import DatabaseConfig

    enabled: t.Optional[bool] = None
    url_prefix: t.Optional[str] = None
    subdomain: t.Optional[str] = None
    url_default: t.Optional[dict] = None
    static_folder: t.Optional[str] = None
    template_folder: t.Optional[str] = None
    static_url_path: t.Optional[str] = None
    root_path: t.Optional[str] = None
    cli_group: t.Optional[str] = None

    init_session: t.Optional[dict] = None

    database_binds: t.Optional[t.Iterable[DatabaseConfig]] = None

    _blueprint_attrs = (
        "url_prefix",
        "subdomain",
        "url_defaults",
        "static_folder",
        "template_folder",
        "static_url_path",
        "root_path",
        "cli_group",
    )

    def __init__(
            self,
            enabled: bool = False,
            url_prefix: str = None,
            subdomain: str = None,
            url_defaults: dict = None,
            static_folder: str = "static",
            template_folder: str = "templates",
            static_url_path: str = "/static",
            root_path: str = None,
            cli_group: str = None,
            init_session: dict = None,
            database_binds: t.Iterable[DatabaseConfig] = None,
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

    def super_settings(self) -> dict:
        return {
            k: getattr(self, k)
            for k in self._blueprint_attrs
            if getattr(self, k)
        }
