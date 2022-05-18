from .. import db


class Example3(db.Model):
    __bind_key__ = "sqldatabase"
    __tablename__ = "example3"
    example2_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
