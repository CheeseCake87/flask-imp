from . import db

sql_do = db.session


class FlSystem(db.Model):
    __tablename__ = "fl_system"
    system_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)


class FlSystemSettings(db.Model):
    __tablename__ = "fl_system_settings"
    system_settings_id = db.Column(db.Integer, primary_key=True)
    setup = db.Column(db.Boolean)
