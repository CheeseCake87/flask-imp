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
        enabled: bool = False,
        dialect: t.Literal[
            "mysql", "postgresql", "sqlite", "oracle", "mssql"
        ] = "sqlite",
        name: str = "database",
        bind_key: str = "",
        location: str = "",
        port: int = 0,
        username: str = "",
        password: str = "",
    ):
        if dialect not in self._allowed_dialects:
            raise ValueError(
                f"Database dialect must be one of: {', '.join(self._allowed_dialects)}"
            )

        self.enabled = enabled
        self.dialect = dialect
        self.name = name
        self.bind_key = bind_key
        self.location = location
        self.port = port
        self.username = username
        self.password = password

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
