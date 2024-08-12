import typing as t
from pathlib import Path


class SQLiteDatabaseConfig:
    enabled: bool
    bind_key: t.Optional[str]
    name: str
    sqlite_db_extension: str
    location: t.Optional[Path]

    def __init__(
        self,
        enabled: bool = True,
        name: str = "database",
        bind_key: str = "",
        sqlite_db_extension: str = ".sqlite",
        location: t.Optional[Path] = None,
    ):
        """
        SQLite database configuration

        Database will be stored in the app instance path if no location is provided
        """
        self.enabled = enabled
        self.name = name
        self.bind_key = bind_key
        self.sqlite_db_extension = sqlite_db_extension
        self.location = location

    def as_dict(self) -> t.Dict[str, t.Any]:
        return {
            "enabled": self.enabled,
            "name": self.name,
            "bind_key": self.bind_key,
            "location": self.location,
            "sqlite_db_extension": self.sqlite_db_extension,
        }

    def uri(self, app_instance_path: Path) -> str:
        if isinstance(self.location, Path):
            if not self.location.exists():
                raise FileNotFoundError(f"Location {self.location} does not exist")

            filepath = self.location / f"{self.name}{self.sqlite_db_extension}"
        else:
            filepath = app_instance_path / f"{self.name}{self.sqlite_db_extension}"

        return f"sqlite:///{filepath}"
