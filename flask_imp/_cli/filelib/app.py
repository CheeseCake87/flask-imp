from dataclasses import dataclass


@dataclass(frozen=True)
class AppFileLib:
    # Format to: app_name, secret_key
    init_py = """\
from flask import Flask
from flask_imp.config import FlaskConfig, ImpConfig, DatabaseConfig
from {app_name}.extensions import imp, db

flask_config = FlaskConfig(
    SECRET_KEY="{secret_key}",
)

imp_config = ImpConfig(
    init_session={{"logged_in": False}},
    database_main=DatabaseConfig(
        enabled=True,
        dialect="sqlite",
    )
)

def create_app():
    app = Flask(__name__, static_url_path="/")
    flask_config.apply_config(app)
    
    imp.init_app(app)
    imp.import_app_resources()
    imp.import_blueprints("blueprints")
    imp.import_models("models")
    db.init_app(app)

    return app
"""

    slim_init_py = """\
from flask import Flask
from flask_imp.config import FlaskConfig
from {app_name}.extensions import imp

flask_config = FlaskConfig(
    SECRET_KEY="{secret_key}",
)

def create_app():
    app = Flask(__name__, static_url_path="/")
    flask_config.apply_config(app)
    
    imp.init_app(app)
    imp.import_app_resources()
    imp.import_blueprint("www")

    return app
"""

    minimal_init_py = """\
from flask import Flask
from flask_imp.config import FlaskConfig
from {app_name}.extensions import imp

flask_config = FlaskConfig(
    SECRET_KEY="{secret_key}",
)

def create_app():
    app = Flask(__name__, static_url_path="/")
    flask_config.apply_config(app)
    
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
