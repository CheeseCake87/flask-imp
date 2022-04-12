from . import db

sql_do = db.session


class FlAdministrator(db.Model):
    __tablename__ = "fl_administrator_permissions"
    administrator_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer)

