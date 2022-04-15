from . import db

sql_do = db.session


class FlAdministrator(db.Model):
    __tablename__ = "fl_administrator"
    administrator_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
