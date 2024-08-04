from flask_imp import DatabaseConfig
from flask_imp import FlaskConfig
from flask_imp import ImpConfig

flask_config = FlaskConfig(
    debug=True,
    secret_key="secret_key",
)

imp_config = ImpConfig(
    init_session={
        "logged_in": False,
    },
    database_main=DatabaseConfig(
        enabled=True,
        dialect="sqlite",
    )
)
