from flask import redirect
from flask import session
from flask import url_for

from ...._flask_launchpad.src.flask_launchpad import model_class
from ...._flask_launchpad.src.flask_launchpad import sql_do

from ....builtins.functions.security import login_required

from .. import bp

FlPermission = model_class("FlPermission")
FlPermissionMembership = model_class("FlPermissionMembership")


@bp.route("/permissions/delete/<permission_id>", methods=["GET"])
@login_required("auth", "account.login")
def delete_permission(permission_id):
    sql_do.query(FlPermissionMembership).filter(
        FlPermissionMembership.permission_id == permission_id
    ).delete()

    sql_do.query(FlPermission).filter(
        FlPermission.permission_id == permission_id
    ).delete()

    sql_do.commit()
    return redirect(url_for("administrator.permissions"))
