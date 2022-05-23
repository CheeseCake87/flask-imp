from flask import current_app

from ..._flask_launchpad.src.flask_launchpad import model_class
from ..._flask_launchpad.src.flask_launchpad import sql_do

FlPermission = model_class("FlPermission", app=current_app)
FlPermissionMembership = model_class("FlPermissionMembership", app=current_app)


def get_permission_membership_from_user_id(user_id: int) -> dict:
    """
    Gets a tuple list of permissions that the user is a member of
    :param user_id: int
    :return: dict {permission name = permission id}, {permission name = permission id},
    """
    users_permissions = sql_do.query(
        FlPermissionMembership
    ).filter(
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
