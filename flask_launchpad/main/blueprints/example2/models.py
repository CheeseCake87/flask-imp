from . import db

sql_do = db.session


class Example2(db.Model):
    __tablename__ = "example2"
    account_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    salt = db.Column(db.String(4), nullable=False)
    private_key = db.Column(db.String(256), nullable=False)
