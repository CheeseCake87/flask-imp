from flask import redirect
from flask import url_for

from .. import FlMembership
from .. import bp
from .. import sql_do
from ....builtins.functions.security import login_required


@bp.route("/users/edit/<user_id>/delete/group/<group_id>", methods=["GET"])
@login_required("auth", "account.login")
def delete_group_from_user(user_id, group_id):
    sql_do.query(
        FlMembership
    ).filter(
        FlMembership.group_id == group_id,
        FlMembership.user_id == user_id
    ).delete()
    sql_do.commit()
    return redirect(url_for("administrator.edit_user", user_id=user_id))
