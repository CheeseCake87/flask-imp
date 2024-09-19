import typing as t
from pathlib import Path


class DatabaseConfig:
    enabled: bool
    dialect: t.Literal["mysql", "postgresql", "sqlite", "oracle", "mssql"]
    bind_key: t.Optional[str]
    name: str
    location: str
    port: int
    username: str
    password: str

    sqlite_db_extension: str

    allowed_dialects: t.Tuple[str, ...] = (
        "mysql",
        "postgresql",
        "sqlite",
        "oracle",
        "mssql",
    )

    def __init__(
        self,
        enabled: bool = True,
        dialect: t.Literal[
            "mysql", "postgresql", "sqlite", "oracle", "mssql"
        ] = "sqlite",
        name: str = "database",
        bind_key: str = "",
        location: str = "",
        port: int = 0,
        username: str = "",
        password: str = "",
        sqlite_db_extension: str = ".sqlite",
    ):
        """
        Database configuration

        Allowed dialects: mysql, postgresql, sqlite, oracle, mssql

        sqlite database will be stored in the app instance path.
        """
        if dialect not in self.allowed_dialects:
            raise ValueError(
                f"Database dialect must be one of: {', '.join(self.allowed_dialects)}"
            )

        self.enabled = enabled
        self.dialect = dialect
        self.name = name
        self.bind_key = bind_key
        self.location = location
        self.port = port
        self.username = username
        self.password = password

        self.sqlite_db_extension = sqlite_db_extension

    def as_dict(self) -> t.Dict[str, t.Any]:
        return {
            "enabled": self.enabled,
            "dialect": self.dialect,
            "name": self.name,
            "bind_key": self.bind_key,
            "location": self.location,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "sqlite_db_extension": self.sqlite_db_extension,
        }

    def uri(self, app_instance_path: Path) -> str:
        if self.dialect == "sqlite":
            filepath = app_instance_path / (self.name + self.sqlite_db_extension)
            return f"{self.dialect}:///{filepath}"

        return (
            f"{self.dialect}://{self.username}:"
            f"{self.password}@{self.location}:"
            f"{self.port}/{self.name}"
        )
