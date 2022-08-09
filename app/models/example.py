from app import bapp
from sqlalchemy import ForeignKey

db = bapp.db


class ExampleUser(db.Model):
    __tablename__ = "fl_example_user"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    salt = db.Column(db.String(4), nullable=False)
    private_key = db.Column(db.String(256), nullable=False)
    disabled = db.Column(db.Boolean)


class ExampleTable(db.Model):
    __tablename__ = "fl_example_table"
    example_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('fl_example_user.user_id'))
    thing = db.Column(db.String(256), nullable=False)
