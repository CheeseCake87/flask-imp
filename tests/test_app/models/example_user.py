from sqlalchemy.orm import relationship

from ..extensions import db


class ExampleUser(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    salt = db.Column(db.String(4), nullable=False)
    private_key = db.Column(db.String(256), nullable=False)
    disabled = db.Column(db.Boolean)

    rel_example_table = relationship(
        "ExampleTable",
        lazy="joined",
        order_by="ExampleTable.thing",
    )

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
