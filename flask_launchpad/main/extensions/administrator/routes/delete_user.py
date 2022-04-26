from flask import redirect
from flask import url_for
from flask import session

from ....builtins.functions.security import login_required

from .. import FlPermissionMembership
from .. import FlUser
from .. import bp
from .. import sql_do


@bp.route("/users/delete/<user_id>", methods=["GET"])
@login_required("auth", "account.login")
def delete_user(user_id):
    if session["user_id"] == user_id:
        session["error"] = "You are not able to delete your own account!"
        return redirect(url_for("administrator.users"))

    sql_do.query(FlUser).filter(
        FlUser.user_id == user_id
    ).delete()
    sql_do.query(FlPermissionMembership).filter(
        FlPermissionMembership.user_id == user_id
    ).delete()
    sql_do.commit()
    return redirect(url_for("administrator.users"))
