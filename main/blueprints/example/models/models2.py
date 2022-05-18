from sqlalchemy import ForeignKey
from .. import db


class Example2(db.Model):
    __tablename__ = "example2"
    example2_id = db.Column(db.Integer, primary_key=True)
    example1_id = db.Column(db.Integer, ForeignKey('example1.example1_id'))
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
