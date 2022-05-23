from flask import redirect
from flask import url_for
from flask import session

from ...._flask_launchpad.src.flask_launchpad import model_class
from ...._flask_launchpad.src.flask_launchpad import sql_do

from ....builtins.functions.security import login_required

from .. import bp

FlUser = model_class("FlUser")
FlPermissionMembership = model_class("FlPermissionMembership")


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
