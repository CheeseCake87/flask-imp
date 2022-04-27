from importlib import import_module
from flask_sqlalchemy import SQLAlchemy

from ...builtins.functions.database import find_model_location

administrator_model = import_module(find_model_location("administrator"))
FlPermissionMembership = getattr(administrator_model, "FlPermissionMembership")
FlCompanyMembership = getattr(administrator_model, "FlCompanyMembership")
FlTeamMembership = getattr(administrator_model, "FlTeamMembership")

db = SQLAlchemy()
sql_do = db.session


def get_permission_membership_from_user_id(user_id: int) -> list:
    """
    Gets a tuple list of permissions that the user is a member of
    :param user_id: int
    :return: list [ tuple (permission_id, permission.name)]
    """
    query_object = sql_do.query(FlPermissionMembership).filter(FlPermissionMembership.user_id == user_id).all()
    permissions = []
    for row in query_object:
        permissions.append((row.permission_id, row._fl_permission.name))
    return permissions


def get_permission_names(user_id: int) -> list:
    permissions = sql_do.query(FlPermissionMembership).filter(FlPermissionMembership.user_id == user_id).all()

    return permissions


def get_companies(user_id: int) -> list:
    return sql_do.query(FlCompanyMembership).filter(FlCompanyMembership.user_id == user_id).all()


def get_company_membership_from_user_id(user_id: int) -> list:
    """
    Gets a tuple list of companies that the user is a member of
    :param user_id: int
    :return: list [ tuple (company_id, company_name)]
    """
    query_object = sql_do.query(FlCompanyMembership).filter(FlCompanyMembership.user_id == user_id).all()
    companies = []
    for row in query_object:
        companies.append((row.company_id, row._fl_company.name))
    return companies


def get_user_ids_from_company_id_list(companies: list) -> list:
    query_object = sql_do.query(FlCompanyMembership.user_id).filter(
        FlCompanyMembership.company_id.in_(companies)
    ).all()
    user_ids = []
    for row in query_object:
        user_ids.append(row.user_id)
    return user_ids


def get_teams(user_id: int) -> list:
    return sql_do.query(FlTeamMembership).filter(FlTeamMembership.user_id == user_id).all()
