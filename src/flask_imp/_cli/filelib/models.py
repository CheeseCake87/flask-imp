def models_example_user_table_py(app_name: str) -> str:
    return f"""\
from sqlalchemy import select, update, delete, insert

from {app_name}.extensions import db
from flask_imp.auth import (
    authenticate_password,
    encrypt_password,
    generate_private_key,
    generate_salt,
)


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
