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


# A user in a Company is unable to see anything from another Company
class FlCompany(db.Model):
    __tablename__ = "fl_company"
    company_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    _fl_company_membership = relationship("FlCompanyMembership", back_populates="_fl_company")


class FlCompanyMembership(db.Model):
    __tablename__ = "fl_company_membership"
    company_membership_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    company_id = db.Column(db.Integer, ForeignKey('fl_company.company_id'))
    _fl_company = relationship("FlCompany", back_populates="_fl_company_membership")


# A user in a Teams are able to scope data
class FlTeam(db.Model):
    __tablename__ = "fl_team"
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    _fl_team_membership = relationship("FlTeamMembership", back_populates="_fl_team")


class FlTeamMembership(db.Model):
    __tablename__ = "fl_team_membership"
    team_membership_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    team_id = db.Column(db.Integer, ForeignKey('fl_team.team_id'))
    _fl_team = relationship("FlTeam", back_populates="_fl_team_membership")
