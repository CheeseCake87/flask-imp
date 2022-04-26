from importlib import import_module
from flask_sqlalchemy import SQLAlchemy

from ...builtins.functions.database import find_model_location

administrator_model = import_module(find_model_location("administrator"))
FlPermissionMembership = getattr(administrator_model, "FlPermissionMembership")
FlCompanyMembership = getattr(administrator_model, "FlCompanyMembership")
FlTeamMembership = getattr(administrator_model, "FlTeamMembership")

db = SQLAlchemy()
sql_do = db.session


def get_permission_membership(user_id: int) -> list:
    return sql_do.query(FlPermissionMembership).filter(FlPermissionMembership.user_id == user_id).all()


def get_permission_names(user_id: int) -> list:
    permissions = sql_do.query(FlPermissionMembership).filter(FlPermissionMembership.user_id == user_id).all()

    return permissions


def get_companies(user_id: int) -> list:
    return sql_do.query(FlCompanyMembership).filter(FlCompanyMembership.user_id == user_id).all()


def get_company_names(user_id: int) -> list:
    memberships = sql_do.query(FlCompanyMembership).filter(FlCompanyMembership.user_id == user_id).all()
    companies = []
    for row in memberships:
        companies.append(row._fl_company.name)
    return companies


def get_teams(user_id: int) -> list:
    return sql_do.query(FlTeamMembership).filter(FlTeamMembership.user_id == user_id).all()
