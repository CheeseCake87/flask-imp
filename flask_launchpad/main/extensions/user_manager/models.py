from . import db

sql_do = db.session


class UserManagerAccount(db.Model):
    __tablename__ = "user_manager_account"
    account_id = db.Column(db.Integer, primary_key=True)
    account_permissions = db.Column(db.Text)
    account_type = db.Column(db.Text)
    username = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    salt = db.Column(db.String(4), nullable=False)
    private_key = db.Column(db.String(256), nullable=False)


class UserManagerGroup(db.Model):
    __tablename__ = "user_manager_group"
    group_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer)
    group_permissions = db.Column(db.Text)
    group_type = db.Column(db.Text)
    group_name = db.Column(db.Text)

