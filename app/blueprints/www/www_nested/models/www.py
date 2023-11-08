from app.extensions import db


class WwwTable(db.Model):
    __bind_key__ = 'www_nested'

    www_id = db.Column(db.Integer, primary_key=True)
    www_name = db.Column(db.String(256), nullable=False)
