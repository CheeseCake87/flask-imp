import typing as t

from flask_imp.config import DatabaseConfig, SQLiteDatabaseConfig, SQLDatabaseConfig


class ImpConfig:
    IMP_INIT_SESSION: t.Optional[t.Dict[str, t.Any]]

    IMP_DATABASE_MAIN: t.Optional[
        t.Union[DatabaseConfig, SQLiteDatabaseConfig, SQLDatabaseConfig]
    ]
    IMP_DATABASE_BINDS: t.Optional[
        t.List[t.Union[DatabaseConfig, SQLiteDatabaseConfig, SQLDatabaseConfig]]
    ]

    def __init__(
        self,
        init_session: t.Optional[t.Dict[str, t.Any]] = None,
        database_main: t.Optional[
            t.Union[DatabaseConfig, SQLiteDatabaseConfig, SQLDatabaseConfig]
        ] = None,
        database_binds: t.Optional[
            t.List[t.Union[DatabaseConfig, SQLiteDatabaseConfig, SQLDatabaseConfig]]
        ] = None,
    ):
        if not init_session:
            self.IMP_INIT_SESSION = {}
        else:
            self.IMP_INIT_SESSION = init_session

        self.IMP_DATABASE_MAIN = database_main

        if database_binds:
            self.IMP_DATABASE_BINDS = database_binds
        else:
            self.IMP_DATABASE_BINDS = []
