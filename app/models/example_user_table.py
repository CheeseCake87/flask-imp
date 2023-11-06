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
        from flask_imp.auth import Auth

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
