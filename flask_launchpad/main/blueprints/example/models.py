from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from . import db

sql_do = db.session


class Example1(db.Model):
    __tablename__ = "example1"
    example1_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    fk_details = relationship("Details")


class Example2(db.Model):
    __tablename__ = "example2"
    example2_id = db.Column(db.Integer, primary_key=True)
    example1_id = db.Column(db.Integer, ForeignKey('example1.example1_id'))
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

