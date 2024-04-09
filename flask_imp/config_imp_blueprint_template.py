import typing as t
from dataclasses import dataclass

from flask_imp import DatabaseConfigTemplate


@dataclass
class ImpBlueprintConfigTemplate:
    """
    ENABLED: bool
    URL_PREFIX: str
    SUBDOMAIN: str
    URL_DEFAULTS: dict
    STATIC_FOLDER: str
    TEMPLATE_FOLDER: str
    STATIC_URL_PATH: str
    ROOT_PATH: str
    CLI_GROUP: str

    INIT_SESSION: dict

    DATABASE_BINDS: t.Optional[
        t.Union[dict,t.List[DatabaseConfig]]
    ]
    """

    ENABLED: t.Optional[bool] = None
    URL_PREFIX: t.Optional[str] = None
    SUBDOMAIN: t.Optional[str] = None
    URL_DEFAULTS: t.Optional[dict] = None
    STATIC_FOLDER: t.Optional[str] = None
    TEMPLATE_FOLDER: t.Optional[str] = None
    STATIC_URL_PATH: t.Optional[str] = None
    ROOT_PATH: t.Optional[str] = None
    CLI_GROUP: t.Optional[str] = None

    INIT_SESSION: t.Optional[dict] = None

    DATABASE_BINDS: t.Optional[t.Set[DatabaseConfigTemplate]] = None

    _attrs = (
        "ENABLED",
        "URL_PREFIX",
        "SUBDOMAIN",
        "URL_DEFAULTS",
        "STATIC_FOLDER",
        "TEMPLATE_FOLDER",
        "STATIC_URL_PATH",
        "ROOT_PATH",
        "CLI_GROUP",
    )

    _known_funcs = ("set_using_args", "set_app_config")

    _blueprint_attrs = (
        "URL_PREFIX",
        "SUBDOMAIN",
        "URL_DEFAULTS",
        "STATIC_FOLDER",
        "TEMPLATE_FOLDER",
        "STATIC_URL_PATH",
        "ROOT_PATH",
        "CLI_GROUP",
    )

    def __init__(self):
        for attr in self._attrs:
            setattr(self, attr, None)

    def set_using_args(
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
            **kwargs,
    ):
        if enabled is not None:
            self.ENABLED = enabled
        if url_prefix is not None:
            self.URL_PREFIX = url_prefix
        if subdomain is not None:
            self.SUBDOMAIN = subdomain
        if url_defaults is not None:
            self.URL_DEFAULTS = url_defaults
        if static_folder is not None:
            self.STATIC_FOLDER = static_folder
        if template_folder is not None:
            self.TEMPLATE_FOLDER = template_folder
        if static_url_path is not None:
            self.STATIC_URL_PATH = static_url_path
        if root_path is not None:
            self.ROOT_PATH = root_path
        if cli_group is not None:
            self.CLI_GROUP = cli_group

        _ = kwargs

    def super_settings(self) -> dict:
        return {
            k.lower(): getattr(self, k)
            for k in self._blueprint_attrs
            if getattr(self, k)
        }
