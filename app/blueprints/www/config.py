from flask_imp import ImpBlueprintConfig, DatabaseConfig


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

    INIT_SESSION: dict = {
        "www_session": "yes"
    }

    DATABASE_BINDS: set[DatabaseConfig] = {
        DatabaseConfig(
            ENABLED=True,
            DIALECT="sqlite",
            NAME="www",
            BIND_KEY="www",
            LOCATION="",
            PORT=0,
            USERNAME="",
            PASSWORD="",
        )
    }
