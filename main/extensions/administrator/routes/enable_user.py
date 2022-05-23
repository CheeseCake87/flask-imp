from flask import redirect
from flask import session
from flask import url_for
from sqlalchemy.orm.exc import NoResultFound

from ...._flask_launchpad.src.flask_launchpad import model_class
from ...._flask_launchpad.src.flask_launchpad import sql_do

from ....builtins.functions.security import login_required

from .. import bp

FlUser = model_class("FlUser")


@bp.route("/users/enable/<user_id>", methods=["GET"])
@login_required("auth", "account.login")
def enable_user(user_id):
    try:
        query_enable_user = sql_do.query(
            FlUser
        ).filter(
            FlUser.user_id == user_id
        ).first()
    except NoResultFound:
        session["error"] = f"No user found using the user_id {user_id}"
        return redirect(url_for("administrator.users"))

    if query_enable_user is None:
        session["error"] = f"No user found using the user_id {user_id}"
        return redirect(url_for("administrator.users"))

    query_enable_user.disabled = False
    sql_do.commit()
    return redirect(url_for("administrator.edit_user", user_id=user_id))
