from flask import redirect
from flask import url_for

from ...._flask_launchpad.src.flask_launchpad import model_class
from ...._flask_launchpad.src.flask_launchpad import sql_do

from ....builtins.functions.security import login_required

from .. import bp

FlPermissionMembership = model_class("FlPermissionMembership")


@bp.route("/users/edit/<user_id>/delete/permissions/<permission_id>", methods=["GET"])
@login_required("auth", "account.login")
def delete_permission_from_user(user_id, permission_id):
    sql_do.query(FlPermissionMembership).filter(
        FlPermissionMembership.permission_id == permission_id,
        FlPermissionMembership.user_id == user_id
    ).delete()
    sql_do.commit()
    return redirect(url_for("administrator.edit_user", user_id=user_id))
