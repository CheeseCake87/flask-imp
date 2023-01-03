from sqlalchemy import ForeignKey

from app import db


class ExampleTableFour(db.Model):
    __tablename__ = "fl_example_table_four"
    example_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('fl_example_user.user_id'))
    thing = db.Column(db.String(256), nullable=False)
