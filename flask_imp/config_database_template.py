import typing as t


class DatabaseConfigTemplate:
    """
    Defaults to sqlite database
    """

    enabled: bool = False
    dialect: t.Literal["mysql", "postgresql", "sqlite", "oracle", "mssql"] = "sqlite"
    bind_key: str = None
    name: str = "database"
    location: str = ""
    port: int = 0
    username: str = ""
    password: str = ""

    _allowed_dialects = ("mysql", "postgresql", "sqlite", "oracle", "mssql")

    def __init__(
        self,
        ENABLED: bool = False,
        DIALECT: t.Literal[
            "mysql", "postgresql", "sqlite", "oracle", "mssql"
        ] = "sqlite",
        NAME: str = "database",
        BIND_KEY: str = "",
        LOCATION: str = "",
        PORT: int = 0,
        USERNAME: str = "",
        PASSWORD: str = "",
    ):
        if DIALECT not in self._allowed_dialects:
            raise ValueError(
                f"Database dialect must be one of: {', '.join(self._allowed_dialects)}"
            )

        self.enabled = ENABLED
        self.dialect = DIALECT
        self.name = NAME
        self.bind_key = BIND_KEY
        self.location = LOCATION
        self.port = PORT
        self.username = USERNAME
        self.password = PASSWORD

    def as_dict(self) -> dict:
        return {
            "enabled": self.enabled,
            "dialect": self.dialect,
            "name": self.name,
            "bind_key": self.bind_key,
            "location": self.location,
            "port": self.port,
            "username": self.username,
            "password": self.password,
        }
