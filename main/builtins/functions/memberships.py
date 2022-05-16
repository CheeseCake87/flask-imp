from importlib import import_module
from flask_sqlalchemy import SQLAlchemy

from ...builtins.functions.database import find_model_location

administrator_model = import_module(find_model_location("administrator"))
FlPermission = getattr(administrator_model, "FlPermission")
FlPermissionMembership = getattr(administrator_model, "FlPermissionMembership")

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



