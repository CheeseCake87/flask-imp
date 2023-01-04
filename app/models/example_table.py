from sqlalchemy import ForeignKey

from app import db
from flask_bigapp.utilities import class_field


class ExampleTable(db.Model):
    example_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(class_field("ExampleUser", "user_id")))
    thing = db.Column(db.String(256), nullable=False)


class ExampleTableOne(db.Model):
    example_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(class_field("ExampleUser", "user_id")))
    thing = db.Column(db.String(256), nullable=False)
