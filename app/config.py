from flask_imp import (
    FlaskConfig,
    ImpConfig,
    DatabaseConfig
)


class Config(ImpConfig):
    FLASK = FlaskConfig(
        # DEBUG=False,
        # PROPAGATE_EXCEPTIONS = True,
        TRAP_HTTP_EXCEPTIONS=False,
        # TRAP_BAD_REQUEST_ERRORS = True,
        SECRET_KEY="flask-imp",  # CHANGE ME
        SESSION_COOKIE_NAME="session",
        # SESSION_COOKIE_DOMAIN = "domain-here.com",
        # SESSION_COOKIE_PATH = "/",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_SAMESITE="Lax",
        PERMANENT_SESSION_LIFETIME=3600,  # 1 hour,
        SESSION_REFRESH_EACH_REQUEST=True,
        USE_X_SENDFILE=False,
        # SEND_FILE_MAX_AGE_DEFAULT = 43200,
        ERROR_404_HELP=True,
        # SERVER_NAME = "localhost:5000",
        APPLICATION_ROOT="/",
        PREFERRED_URL_SCHEME="http",
        # MAX_CONTENT_LENGTH = 0,
        # TEMPLATES_AUTO_RELOAD = True,
        EXPLAIN_TEMPLATE_LOADING=False,
        MAX_COOKIE_SIZE=4093,
    )

    # INIT_SESSION = {
    #     "logged_in": False,
    # }

    # Below are extra settings that Flask-Imp uses but relates to Flask-SQLAlchemy.
    # This sets the file extension for SQLite databases, and where to create the folder
    # that the database will be stored in.
    # True will create the folder on the same level as your
    # app, False will create the folder in the app root.
    SQLITE_DB_EXTENSION = ".sqlite"
    SQLITE_STORE_IN_PARENT = False
    #

    # SQLAlchemy settings that will be passed to Flask
    # Any SQLAlchemy setting here will overwrite anything
    # set in the config above
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False
    #

    # Main database settings, this will be turned int the SQLALCHEMY_DATABASE_URI
    # DATABASE_MAIN = DatabaseConfig(
    #     enabled=True,
    #     dialect="sqlite",
    #     name="main",
    #     location="",
    #     port=0,
    #     username="",
    #     password="",
    # )

    # Binds are additional databases that can be used in your app
    # These will be added to the SQLALCHEMY_BINDS dictionary
    # DATABASE_BINDS = {
    #     DatabaseConfig(
    #         enabled=True,
    #         dialect="sqlite",
    #         name="additional_database",
    #         bind_key="additional_database",
    #         location="",
    #         port=0,
    #         username="",
    #         password="",
    #     )
    # }
