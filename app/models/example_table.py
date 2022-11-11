from sqlalchemy import ForeignKey

from app import db


class ExampleTable(db.Model):
    __tablename__ = "fl_example_table"
    example_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('fl_example_user.user_id'))
    thing = db.Column(db.String(256), nullable=False)
