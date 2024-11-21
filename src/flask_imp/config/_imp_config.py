from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from flask_imp.config import DatabaseConfig, SQLiteDatabaseConfig, SQLDatabaseConfig


class ImpConfig:
    """
    Imp configuration class.
    """

    IMP_INIT_SESSION: t.Optional[t.Dict[str, t.Any]]

    IMP_DATABASE_MAIN: t.Optional[
        t.Union[DatabaseConfig, SQLiteDatabaseConfig, SQLDatabaseConfig]
    ]
    IMP_DATABASE_BINDS: t.Optional[
        t.Iterable[t.Union[DatabaseConfig, SQLiteDatabaseConfig, SQLDatabaseConfig]]
    ]

    def __init__(
        self,
        init_session: t.Optional[t.Dict[str, t.Any]] = None,
        database_main: t.Optional[
            t.Union[DatabaseConfig, SQLiteDatabaseConfig, SQLDatabaseConfig]
        ] = None,
        database_binds: t.Optional[
            t.Iterable[t.Union[DatabaseConfig, SQLiteDatabaseConfig, SQLDatabaseConfig]]
        ] = None,
    ):
        """
        The Imp configuration class.

        This class is used to configure the global session cookie values
        used by your application.

        It's also used to store any database configurations that are
        used by Flask-SQLAlchemy.

        :param init_session: The initial session dictionary.
        :param database_main: The main database configuration.
        :param database_binds: An iterable of database bind configurations.
        """
        if not init_session:
            self.IMP_INIT_SESSION = {}
        else:
            self.IMP_INIT_SESSION = init_session

        self.IMP_DATABASE_MAIN = database_main

        if database_binds:
            self.IMP_DATABASE_BINDS = database_binds
        else:
            self.IMP_DATABASE_BINDS = []
