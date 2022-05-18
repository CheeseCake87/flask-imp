from sqlalchemy.orm import relationship
from .. import db


class Example1(db.Model):
    __tablename__ = "example1"
    example1_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    fk_details = relationship("Example2")
