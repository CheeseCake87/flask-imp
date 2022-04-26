from flask import redirect
from flask import session
from flask import url_for

from ....builtins.functions.security import login_required

from .. import FlUser
from .. import bp
from .. import sql_do


@bp.route("/users/disable/<user_id>", methods=["GET"])
@login_required("auth", "account.login")
def disable_user(user_id):
    query_disable_user = sql_do.query(FlUser).filter(
        FlUser.user_id == user_id
    ).first()

    if query_disable_user is None:
        session["error"] = f"No user found using the user_id {user_id}"
        return redirect(url_for("administrator.users"))

    query_disable_user.disabled = True
    sql_do.commit()
    return redirect(url_for("administrator.edit_user", user_id=user_id))
