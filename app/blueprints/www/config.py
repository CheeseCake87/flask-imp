from flask_imp import ImpBlueprintConfig


class Config(ImpBlueprintConfig):
    ENABLED: bool = True
    URL_PREFIX: str = "/"
    # SUBDOMAIN: str = ""
    # URL_DEFAULTS: dict = {}
    STATIC_FOLDER: str = "static"
    TEMPLATE_FOLDER: str = "templates"
    STATIC_URL_PATH: str = "/static"
    # ROOT_PATH: str = ""
    # CLI_GROUP: str = ""

    INIT_SESSION: dict = {}

    DATABASE_BINDS = None
