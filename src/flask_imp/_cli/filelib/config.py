def config_init_full_py(app_name: str) -> str:
    return f"""\
from flask_imp.config import ImpConfig, FlaskConfig, DatabaseConfig
from {app_name}.globals import FLASK_SECRET_KEY


# !!! MOVE secret_key TO .env FILE
FLASK_CONFIG = FlaskConfig(
    secret_key=FLASK_SECRET_KEY
)

IMP_CONFIG = ImpConfig(
    init_session={{"logged_in": False}},
    database_main=DatabaseConfig(
        enabled=True,
        dialect="sqlite"
    )
)
"""


def config_init_slim_or_minimal_py(app_name: str) -> str:
    return f"""\
from flask_imp.config import ImpConfig, FlaskConfig
from {app_name}.globals import FLASK_SECRET_KEY


FLASK_CONFIG = FlaskConfig(
    secret_key=FLASK_SECRET_KEY
)

IMP_CONFIG = ImpConfig()
"""
