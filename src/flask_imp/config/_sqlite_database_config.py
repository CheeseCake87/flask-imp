import typing as t
from pathlib import Path


class SQLiteDatabaseConfig:
    database_name: str
    sqlite_db_extension: str
    location: t.Optional[Path]
    bind_key: t.Optional[str]
    enabled: bool

    def __init__(
        self,
        database_name: str = "database",
        sqlite_db_extension: str = ".sqlite",
        location: t.Optional[Path] = None,
        bind_key: t.Optional[str] = None,
        enabled: bool = True,
    ):
        """
        SQLite database configuration

        Database will be stored in the app instance path if no location is provided

        :param database_name: name of the database - defaults to "database"
        :param sqlite_db_extension: extension of the database - defaults to ".sqlite"
        :param location: location of the database - Optional - defaults to app instance path
        :param bind_key: bind key to be used in SQLAlchemy - Optional
        :param enabled: whether the database is enabled - defaults to True
        """
        self.enabled = enabled
        self.database_name = database_name
        self.bind_key = bind_key
        self.sqlite_db_extension = sqlite_db_extension
        self.location = location

    def as_dict(self) -> t.Dict[str, t.Any]:
        return {
            "enabled": self.enabled,
            "database_name": self.database_name,
            "bind_key": self.bind_key,
            "location": self.location,
            "sqlite_db_extension": self.sqlite_db_extension,
        }

    def uri(self, app_instance_path: Path) -> str:
        if isinstance(self.location, Path):
            if not self.location.exists():
                raise FileNotFoundError(f"Location {self.location} does not exist")

            filepath = self.location / f"{self.database_name}{self.sqlite_db_extension}"
        else:
            filepath = (
                app_instance_path / f"{self.database_name}{self.sqlite_db_extension}"
            )

        return f"sqlite:///{filepath}"
