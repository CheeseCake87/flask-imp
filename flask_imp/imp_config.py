import typing as t


class ImpConfig:
    INIT_SESSION: t.Dict[str, t.Union[bool, str, int]]
    SQLALCHEMY: t.Dict[str, t.Union[bool, str, int]]
    DATABASE_MAIN: t.Dict[str, t.Union[bool, str, int]]
    DATABASE_BINDS: t.List[t.Dict[str, t.Union[bool, str, int]]]

    def __init__(
            self,
            init_session: t.Optional[t.Dict[str, t.Union[bool, str, int]]],
            sqlalchemy: t.Optional[t.Dict[str, t.Union[bool, str, int]]],
            database_main: t.Optional[t.Dict[str, t.Union[bool, str, int]]],
            database_binds: t.Optional[t.List[t.Dict[str, t.Union[bool, str, int]]]],
    ):
        self.INIT_SESSION = init_session
        self.SQLALCHEMY = sqlalchemy
        self.DATABASE_MAIN = database_main
        self.DATABASE_BINDS = database_binds

        self._ensure_correct_attributes_for_database()

    def _ensure_correct_attributes_for_database(self):
        if "ENABLED" not in self.DATABASE_MAIN:
            raise AttributeError("ENABLED is required in the database config")
        if "DIALECT" not in self.DATABASE_MAIN:
            raise AttributeError("DIALECT is required in the database config")
        if self.DATABASE_MAIN.get("DIALECT") != "sqlite":
            if "USERNAME" not in self.DATABASE_MAIN:
                raise AttributeError("USERNAME is required in the database config")
            if "PASSWORD" not in self.DATABASE_MAIN:
                raise AttributeError("PASSWORD is required in the database config")
            if "HOST" not in self.DATABASE_MAIN:
                raise AttributeError("HOST is required in the database config")
            if "PORT" not in self.DATABASE_MAIN:
                raise AttributeError("PORT is required in the database config")
            if "DATABASE" not in self.DATABASE_MAIN:
                raise AttributeError("DATABASE is required in the database config")
