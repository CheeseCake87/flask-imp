import typing as t


class SQLDatabaseConfig:
    dialect: t.Literal["mysql", "postgresql", "oracle", "mssql"]
    database_name: str
    location: str
    port: int
    username: str
    password: str
    bind_key: t.Optional[str] = None
    enabled: bool = False

    allowed_dialects: t.Tuple[str, ...] = ("mysql", "postgresql", "oracle", "mssql")

    def __init__(
        self,
        dialect: t.Literal["mysql", "postgresql", "oracle", "mssql"],
        database_name: str,
        location: str,
        port: int,
        username: str,
        password: str,
        bind_key: t.Optional[str] = None,
        enabled: bool = True,
    ) -> None:
        """
        SQL database configuration

        Allowed dialects: mysql, postgresql, oracle, mssql

        :param dialect: database dialect - one of: mysql, postgresql, oracle, mssql
        :param database_name: name of the database
        :param location: location of the database
        :param port: port of the database
        :param username: username to connect to the database
        :param password: password to connect to the database
        :param bind_key: bind key to be used in SQLAlchemy - Optional
        :param enabled: whether the database is available to the application - defaults to True
        """
        if dialect not in self.allowed_dialects:
            raise ValueError(
                f"Database dialect must be one of: {', '.join(self.allowed_dialects)}"
            )

        self.dialect = dialect
        self.enabled = enabled
        self.database_name = database_name
        self.bind_key = bind_key
        self.location = location
        self.port = port
        self.username = username
        self.password = password

    def as_dict(self) -> t.Dict[str, t.Any]:
        return {
            "enabled": self.enabled,
            "dialect": self.dialect,
            "database_name": self.database_name,
            "bind_key": self.bind_key,
            "location": self.location,
            "port": self.port,
            "username": self.username,
            "password": self.password,
        }

    def uri(self) -> str:
        return (
            f"{self.dialect}://{self.username}:"
            f"{self.password}@{self.location}:"
            f"{self.port}/{self.database_name}"
        )
