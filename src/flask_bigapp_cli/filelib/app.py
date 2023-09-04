class AppFileLib:
    # Format to: app_name
    default_config_toml = """\
# Flask-BigApp Config File
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
SECRET_KEY = "super_secret_key"
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

# These settings are spcific to the Flask-SQLAlchemy extension.
# Anything here will be accessible using app.config
[SQLALCHEMY]
SQLALCHEMY_ECHO = false
SQLALCHEMY_TRACK_MODIFICATIONS = false
SQLALCHEMY_RECORD_QUERIES = false

# [DATABASE.MAIN] is loaded as SQLALCHEMY_DATABASE_URI
# Dialets = mysql / postgresql / sqlite / oracle / mssql

# Uncomment below to generate the SQLALCHEMY_DATABASE_URI.
#[DATABASE.MAIN]
#ENABLED = true
#DIALECT = "sqlite"
#DATABASE_NAME = "database"
#LOCATION = "db"
#PORT = ""
#USERNAME = "database"
#PASSWORD = "password"

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
#DATABASE_NAME = "database_another"
#LOCATION = "db"
#PORT = ""
#USERNAME = "user"
#PASSWORD = "password"
"""

    init_py = """\
from flask import Flask
from {app_name}.extensions import bigapp, db


def create_app():
    app = Flask(__name__)
    bigapp.init_app(app)
    #db.init_app(app)

    bigapp.import_app_resources()

    bigapp.import_blueprints("blueprints")

    #bigapp.import_models("models")

    return app
"""

    extensions_init_py = """\
from flask_bigapp import BigApp
from flask_sqlalchemy import SQLAlchemy

bigapp = BigApp()
db = SQLAlchemy()
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
    "relationship",
]
"""

    # Format to: None
    models_example_user_table_py = """\
from . import *


class ExampleUserTable(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    salt = db.Column(db.String(4), nullable=False)
    private_key = db.Column(db.String(256), nullable=False)
    disabled = db.Column(db.Boolean)

    @classmethod
    def get_by_id(cls, user_id):
        return db.session.execute(
            select(cls).filter_by(user_id=user_id).limit(1)
        ).scalar_one_or_none()

    @classmethod
    def create(cls, username, password, disabled):
        from flask_bigapp.auth import Auth

        salt = Auth.generate_salt()
        salt_pepper_password = Auth.hash_password(password, salt)
        private_key = Auth.generate_private_key(username)

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
    def update(cls, user_id, username, private_key, disabled):
        db.session.execute(
            update(cls).where(
                cls.user_id == user_id  # noqa
            ).values(
                username=username,
                private_key=private_key,
                disabled=disabled,
            )
        )
        db.session.commit()

    @classmethod
    def delete(cls, user_id):
        db.session.execute(
            delete(cls).where(
                cls.user_id == user_id  # noqa
            )
        )
        db.session.commit()
"""
