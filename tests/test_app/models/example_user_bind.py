from ..extensions import db


class ExampleUserBind(db.Model):
    __bind_key__ = "another"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    salt = db.Column(db.String(4), nullable=False)
    private_key = db.Column(db.String(256), nullable=False)
    disabled = db.Column(db.Boolean)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
