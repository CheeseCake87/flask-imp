from dataclasses import dataclass


@dataclass(frozen=True)
class AppFileLib:
    # Format to: secret_key
    default_init_config_toml = """\
# Flask-Imp Config File
# ------------------------
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env
# vars it is created and will be accessible using
# app.config. All key names defined below will be
# capitalised when imported.
[FLASK]
DEBUG = false
#PROPAGATE_EXCEPTIONS = true
TRAP_HTTP_EXCEPTIONS = false
#TRAP_BAD_REQUEST_ERRORS = true
SECRET_KEY = "{secret_key}"
SESSION_COOKIE_NAME = "session"
#SESSION_COOKIE_DOMAIN = "domain-here.com"
#SESSION_COOKIE_PATH = "/"
SESSION_COOKIE_HTTPONLY = true
SESSION_COOKIE_SECURE = false
SESSION_COOKIE_SAMESITE = "Lax"
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
SESSION_REFRESH_EACH_REQUEST = true
USE_X_SENDFILE = false
#SEND_FILE_MAX_AGE_DEFAULT = 43200
ERROR_404_HELP = true
#SERVER_NAME = "localhost:5000"
APPLICATION_ROOT = "/"
PREFERRED_URL_SCHEME = "http"
#MAX_CONTENT_LENGTH = 0
#TEMPLATES_AUTO_RELOAD = true
EXPLAIN_TEMPLATE_LOADING = false
MAX_COOKIE_SIZE = 4093

# This will set the default session variables for the app.
# Anything here will be accessible using session["your_var_name"]
# or session.get("your_var_name")
[SESSION]
logged_in = false

# These settings are specific to the Flask-SQLAlchemy extension.
# Anything here will be accessible using app.config
[SQLALCHEMY]
SQLALCHEMY_ECHO = false
SQLALCHEMY_TRACK_MODIFICATIONS = false
SQLALCHEMY_RECORD_QUERIES = false
# Below are extra settings that Flask-Imp uses but relates to Flask-SQLAlchemy.
# This sets the file extension for SQLite databases, and where to create the folder
# that the database will be stored in. true will create the folder on the same level as your
# app, false will create the folder in the app root.
SQLITE_DB_EXTENSION = ".sqlite"
SQLITE_STORE_IN_PARENT = false

# [DATABASE.MAIN] is loaded as SQLALCHEMY_DATABASE_URI
# Dialets = mysql / postgresql / sqlite / oracle / mssql
# Uncomment below to generate the SQLALCHEMY_DATABASE_URI.
[DATABASE.MAIN]
ENABLED = true
DIALECT = "sqlite"
DATABASE_NAME = "database"
LOCATION = ""
PORT = ""
USERNAME = ""
PASSWORD = ""

# Adding another database is as simple as adding a new section.
# [DATABASE.ANOTHER] will then be accessible using SQLALCHEMY_BINDS
# The bind key will be stored as a lowercase value, so "ANOTHER" will
# be accessible as "another"
# You can then use the bind key in the model as follows:
# class MyModel(db.Model):
#     __bind_key__ = "another"
#     ...

# Uncomment below to generate and add to SQLALCHEMY_BINDS.
#[DATABASE.ANOTHER]
#ENABLED = true
#DIALECT = "sqlite"
#DATABASE_NAME = "another"
#LOCATION = ""
#PORT = ""
#USERNAME = ""
#PASSWORD = ""
"""

    # Format to: secret_key
    default_config_toml = """\
# Flask-Imp Config File
# ------------------------
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env
# vars it is created and will be accessible using
# app.config. All key names defined below will be
# capitalised when imported.
[FLASK]
DEBUG = false
#PROPAGATE_EXCEPTIONS = true
TRAP_HTTP_EXCEPTIONS = false
#TRAP_BAD_REQUEST_ERRORS = true
SECRET_KEY = "{secret_key}"
SESSION_COOKIE_NAME = "session"
#SESSION_COOKIE_DOMAIN = "domain-here.com"
#SESSION_COOKIE_PATH = "/"
SESSION_COOKIE_HTTPONLY = true
SESSION_COOKIE_SECURE = false
SESSION_COOKIE_SAMESITE = "Lax"
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
SESSION_REFRESH_EACH_REQUEST = true
USE_X_SENDFILE = false
#SEND_FILE_MAX_AGE_DEFAULT = 43200
ERROR_404_HELP = true
#SERVER_NAME = "localhost:5000"
APPLICATION_ROOT = "/"
PREFERRED_URL_SCHEME = "http"
#MAX_CONTENT_LENGTH = 0
#TEMPLATES_AUTO_RELOAD = true
EXPLAIN_TEMPLATE_LOADING = false
MAX_COOKIE_SIZE = 4093

# This will set the default session variables for the app.
# Anything here will be accessible using session["your_var_name"]
# or session.get("your_var_name")
[SESSION]
#logged_in = false

# These settings are specific to the Flask-SQLAlchemy extension.
# Anything here will be accessible using app.config
[SQLALCHEMY]
SQLALCHEMY_ECHO = false
SQLALCHEMY_TRACK_MODIFICATIONS = false
SQLALCHEMY_RECORD_QUERIES = false
# Below are extra settings that Flask-Imp uses but relates to Flask-SQLAlchemy.
# This sets the file extension for SQLite databases, and where to create the folder
# that the database will be stored in. true will create the folder on the same level as your
# app, false will create the folder in the app root.
SQLITE_DB_EXTENSION = ".sqlite"
SQLITE_STORE_IN_PARENT = false

# [DATABASE.MAIN] is loaded as SQLALCHEMY_DATABASE_URI
# Dialets = mysql / postgresql / sqlite / oracle / mssql
# Uncomment below to generate the SQLALCHEMY_DATABASE_URI.
#[DATABASE.MAIN]
#ENABLED = true
#DIALECT = "sqlite"
#DATABASE_NAME = "database"
#LOCATION = ""
#PORT = ""
#USERNAME = ""
#PASSWORD = ""

# Adding another database is as simple as adding a new section.
# [DATABASE.ANOTHER] will then be accessible using SQLALCHEMY_BINDS
# The bind key will be stored as a lowercase value, so "ANOTHER" will
# be accessible as "another"
# You can then use the bind key in the model as follows:
# class MyModel(db.Model):
#     __bind_key__ = "another"
#     ...

# Uncomment below to generate and add to SQLALCHEMY_BINDS.
#[DATABASE.ANOTHER]
#ENABLED = true
#DIALECT = "sqlite"
#DATABASE_NAME = "another"
#LOCATION = ""
#PORT = ""
#USERNAME = ""
#PASSWORD = ""
"""

    # Format to: app_name
    init_py = """\
from flask import Flask
from {app_name}.extensions import imp, db


def create_app():
    app = Flask(__name__, static_url_path="/")
    imp.init_app(app)
    imp.import_app_resources()
    imp.import_blueprints("blueprints")
    imp.import_models("models")
    db.init_app(app)

    return app
"""

    slim_init_py = """\
from flask import Flask
from {app_name}.extensions import imp


def create_app():
    app = Flask(__name__, static_url_path="/")
    imp.init_app(app)
    imp.import_app_resources()
    imp.import_blueprint("www")

    return app
"""

    minimal_init_py = """\
from flask import Flask
from {app_name}.extensions import imp


def create_app():
    app = Flask(__name__, static_url_path="/")
    imp.init_app(app)
    imp.import_app_resources()

    return app
"""

    extensions_init_py = """\
from flask_imp import Imp
from flask_sqlalchemy import SQLAlchemy

imp = Imp()
db = SQLAlchemy()
"""

    slim_extensions_init_py = """\
from flask_imp import Imp

imp = Imp()
"""

    # Format to: app_name
    models_init_py = """\
from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm import relationship

from {app_name}.extensions import db

__all__ = [
    "db",
    "select",
    "update",
    "delete",
    "insert",
]
"""

    # Format to: None
    models_example_user_table_py = """\
from flask_imp.auth import authenticate_password
from flask_imp.auth import encrypt_password
from flask_imp.auth import generate_private_key
from flask_imp.auth import generate_salt
from . import *


class ExampleUserTable(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    salt = db.Column(db.String(4), nullable=False)
    private_key = db.Column(db.String(256), nullable=False)
    disabled = db.Column(db.Boolean)

    @classmethod
    def login(cls, username, password: str) -> bool:
        user = cls.get_by_username(username)
        if user is None:
            return False
        return authenticate_password(password, user.password, user.salt)

    @classmethod
    def get_by_id(cls, user_id: int):
        return db.session.execute(
            select(cls).filter_by(user_id=user_id).limit(1)
        ).scalar_one_or_none()

    @classmethod
    def get_by_username(cls, username: str):
        return db.session.execute(
            select(cls).filter_by(username=username).limit(1)
        ).scalar_one_or_none()

    @classmethod
    def create(cls, username, password, disabled):
        salt = generate_salt()
        salt_pepper_password = encrypt_password(password, salt)
        private_key = generate_private_key(username)

        db.session.execute(
            insert(cls).values(
                username=username,
                password=salt_pepper_password,
                salt=salt,
                private_key=private_key,
                disabled=disabled,
            )
        )
        db.session.commit()

    @classmethod
    def update(cls, user_id: int, username, private_key, disabled):
        db.session.execute(
            update(cls).where(
                cls.user_id == user_id
            ).values(
                username=username,
                private_key=private_key,
                disabled=disabled,
            )
        )
        db.session.commit()

    @classmethod
    def delete(cls, user_id: int):
        db.session.execute(
            delete(cls).where(
                cls.user_id == user_id
            )
        )
        db.session.commit()
"""
