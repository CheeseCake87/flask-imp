from importlib import import_module
from flask_sqlalchemy import SQLAlchemy

from ...builtins.functions.database import find_model_location

administrator_model = import_module(find_model_location("administrator"))
FlPermission = getattr(administrator_model, "FlPermission")
FlPermissionMembership = getattr(administrator_model, "FlPermissionMembership")
FlCompany = getattr(administrator_model, "FlCompany")
FlCompanyMembership = getattr(administrator_model, "FlCompanyMembership")
FlTeamMembership = getattr(administrator_model, "FlTeamMembership")

db = SQLAlchemy()
sql_do = db.session


def get_permission_membership_from_user_id(user_id: int) -> dict:
    """
    Gets a tuple list of permissions that the user is a member of
    :param user_id: int
    :return: dict {permission name = permission id}, {permission name = permission id},
    """
    users_permissions = sql_do.query(FlPermissionMembership).filter(
        FlPermissionMembership.user_id == user_id
    ).all()
    permissions = {}
    for row in users_permissions:
        permissions[row._fl_permission.name] = row.permission_id
    return permissions


def get_permission_names(user_id: int) -> list:
    permissions = sql_do.query(FlPermissionMembership).filter(FlPermissionMembership.user_id == user_id).all()
    return permissions


def get_permission_id_from_permission_name(permission_name: str) -> str:
    query_object = sql_do.query(FlPermission).filter(
        FlPermission.name == permission_name
    ).first()
    return query_object.permission_id


def get_companies(user_id: int) -> list:
    return sql_do.query(FlCompanyMembership).filter(FlCompanyMembership.user_id == user_id).all()


def get_company_membership_from_user_id(user_id: int) -> dict:
    """
    Returns a dict of companies that the user is a member of
    :param user_id: int
    :return: dict {company name = company id},
    """
    users_companies = sql_do.query(FlCompanyMembership).filter(
        FlCompanyMembership.user_id == user_id
    ).all()
    companies = {}
    for row in users_companies:
        companies[row._fl_company.name] = row.company_id
    return companies


def get_all_companies() -> dict:
    """
    Returns a dict of all companies
    :return: dict {company name = company id},
    """
    all_companies = sql_do.query(FlCompany).all()
    companies = {}
    for row in all_companies:
        companies[row.name] = row.company_id
    return companies


def get_user_ids_from_company_id_list(company_ids: list) -> list:
    """
    Returns a list of user_ids found within membership of a list of companies
    """
    query_object = sql_do.query(FlCompanyMembership.user_id).filter(
        FlCompanyMembership.company_id.in_(company_ids)
    ).all()
    user_ids = []
    for row in query_object:
        user_ids.append(row.user_id)
    return user_ids


def get_teams(user_id: int) -> list:
    return sql_do.query(FlTeamMembership).filter(FlTeamMembership.user_id == user_id).all()
