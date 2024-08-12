import typing as t


class SQLDatabaseConfig:
    enabled: bool = False
    dialect: t.Literal["mysql", "postgresql", "oracle", "mssql"]
    bind_key: t.Optional[str] = None
    name: str = "database"
    location: str = ""
    port: int = 0
    username: str = ""
    password: str = ""

    allowed_dialects: t.Tuple[str, ...] = ("mysql", "postgresql", "oracle", "mssql")

    def __init__(
        self,
        dialect: t.Literal["mysql", "postgresql", "oracle", "mssql"],
        enabled: bool = True,
        name: str = "database",
        bind_key: str = "",
        location: str = "",
        port: int = 0,
        username: str = "",
        password: str = "",
    ):
        """
        SQL database configuration

        Allowed dialects: mysql, postgresql, oracle, mssql
        """
        if dialect not in self.allowed_dialects:
            raise ValueError(
                f"Database dialect must be one of: {', '.join(self.allowed_dialects)}"
            )

        self.dialect = dialect
        self.enabled = enabled
        self.name = name
        self.bind_key = bind_key
        self.location = location
        self.port = port
        self.username = username
        self.password = password

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
        }

    def uri(self) -> str:
        return (
            f"{self.dialect}://{self.username}:"
            f"{self.password}@{self.location}:"
            f"{self.port}/{self.name}"
        )
