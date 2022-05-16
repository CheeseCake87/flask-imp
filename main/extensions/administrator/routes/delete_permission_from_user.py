from flask import redirect
from flask import url_for

from ....builtins.functions.security import login_required

from .. import FlPermissionMembership
from .. import bp
from .. import sql_do


@bp.route("/users/edit/<user_id>/delete/permissions/<permission_id>", methods=["GET"])
@login_required("auth", "account.login")
def delete_permission_from_user(user_id, permission_id):
    sql_do.query(FlPermissionMembership).filter(
        FlPermissionMembership.permission_id == permission_id,
        FlPermissionMembership.user_id == user_id
    ).delete()
    sql_do.commit()
    return redirect(url_for("administrator.edit_user", user_id=user_id))
