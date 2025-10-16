from sqlalchemy import ForeignKey

from ..extensions import db


class ExampleTable(db.Model):
    example_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("example_user.user_id"))
    thing = db.Column(db.String(256), nullable=False)

    @classmethod
    def get_first(cls):
        return cls.query.first()

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def delete(cls, user_id):
        pass

    @classmethod
    def update(cls, user_id, **kwargs):
        pass

    @classmethod
    def add(cls, **kwargs):
        pass


class ExampleTableOne(db.Model):
    example_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("example_user.user_id"))
    thing = db.Column(db.String(256), nullable=False)
