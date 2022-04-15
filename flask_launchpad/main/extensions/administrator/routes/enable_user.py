from ....builtins.functions.security import login_required
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from .. import bp
from .. import struc
from .. import sql_do
from .. import FlUser
from .. import FlGroup
from sqlalchemy.orm.exc import NoResultFound
from flask import render_template
from sqlalchemy import desc
from flask import request
from flask import session
from flask import redirect
from flask import url_for


@bp.route("/users/enable/<user_id>", methods=["GET"])
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
