from . import db

sql_do = db.session


class FlUser(db.Model):
    __tablename__ = "fl_user"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    salt = db.Column(db.String(4), nullable=False)
    private_key = db.Column(db.String(256), nullable=False)
    disabled = db.Column(db.Boolean)


class FlGroup(db.Model):
    __tablename__ = "fl_group"
    group_id = db.Column(db.Integer, primary_key=True)
    group_type = db.Column(db.Text)
    group_name = db.Column(db.Text)


class FlMembership(db.Model):
    __tablename__ = "fl_membership"
    membership_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
