import typing as t
from pathlib import Path


class DatabaseConfig:
    """
    Database configuration class used by ImpConfig, or ImpBlueprintConfig.
    """

    enabled: bool
    dialect: t.Literal["mysql", "postgresql", "sqlite", "oracle", "mssql"]
    bind_key: t.Optional[str]
    database_name: str
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
        dialect: t.Literal[
            "mysql", "postgresql", "sqlite", "oracle", "mssql"
        ] = "sqlite",
        database_name: str = "database",
        location: str = "",
        port: int = 0,
        username: str = "",
        password: str = "",
        sqlite_db_extension: str = ".sqlite",
        bind_key: t.Optional[str] = None,
        enabled: bool = True,
    ):
        """
        Database configuration class used by ImpConfig, or ImpBlueprintConfig.

        Allowed dialects: mysql, postgresql, sqlite, oracle, mssql

        sqlite database will be stored in the app instance path.

        **Note:**

        - If the dialect is sqlite, the location, port, username, and password are not used.

        *Replaced by:*

        - :class:`flask_imp.config.SQLDatabaseConfig`
        - :class:`flask_imp.config.SQLiteDatabaseConfig`

        :param enabled: whether the database is enabled - defaults to True
        :param dialect: the database dialect - defaults to sqlite
        :param name: the database name - defaults to database
        :param bind_key: the database bind key - Optional
        :param location: the database location - Optional
        :param port: the database port - Optional
        :param username: the database username - Optional
        :param password: the database password - Optional
        :param sqlite_db_extension: the sqlite database extension - defaults to .sqlite
        """
        if dialect not in self.allowed_dialects:
            raise ValueError(
                f"Database dialect must be one of: {', '.join(self.allowed_dialects)}"
            )

        self.enabled = enabled
        self.dialect = dialect
        self.database_name = database_name
        self.bind_key = bind_key
        self.location = location
        self.port = port
        self.username = username
        self.password = password

        self.sqlite_db_extension = sqlite_db_extension

    def as_dict(self) -> t.Dict[str, t.Any]:
        """
        Return the database configuration as a dictionary.

        :return: the database configuration as a dictionary
        """
        return {
            "enabled": self.enabled,
            "dialect": self.dialect,
            "database_name": self.database_name,
            "bind_key": self.bind_key,
            "location": self.location,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "sqlite_db_extension": self.sqlite_db_extension,
        }

    def uri(self, app_instance_path: Path) -> str:
        """
        Return the database URI.

        :param app_instance_path: the app instance path
        :return: the database URI
        """
        if self.dialect == "sqlite":
            filepath = app_instance_path / (
                self.database_name + self.sqlite_db_extension
            )
            return f"{self.dialect}:///{filepath}"

        return (
            f"{self.dialect}://{self.username}:"
            f"{self.password}@{self.location}:"
            f"{self.port}/{self.database_name}"
        )
