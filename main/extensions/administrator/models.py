from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from . import db

sql_do = db.session


# Permissions are used to disable certain features
class FlPermission(db.Model):
    __tablename__ = "fl_permission"
    permission_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text)
    name = db.Column(db.Text)
    _fl_permission_membership = relationship("FlPermissionMembership", back_populates="_fl_permission")


class FlPermissionMembership(db.Model):
    __tablename__ = "fl_permission_membership"
    permission_membership_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    permission_id = db.Column(db.Integer, ForeignKey('fl_permission.permission_id'))
    _fl_permission = relationship("FlPermission", back_populates="_fl_permission_membership")
