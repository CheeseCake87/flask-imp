from ....builtins.functions.security import login_required
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from .. import bp
from .. import struc
from .. import sql_do
from .. import FlUser
from .. import FlGroup
from .. import FlMembership
from sqlalchemy.orm.exc import NoResultFound
from flask import render_template
from sqlalchemy import desc
from flask import request
from flask import session
from flask import redirect
from flask import url_for


@bp.route("/users/delete/<user_id>", methods=["GET"])
def delete_user(user_id):
    try:
        query_delete_user = sql_do.query(
            FlUser
        ).filter(
            FlUser.user_id == user_id
        ).first()
    except NoResultFound:
        session["error"] = f"No user found using the user_id {user_id}"
        return redirect(url_for("administrator.users"))

    if query_delete_user is None:
        session["error"] = f"No user found using the user_id {user_id}"
        return redirect(url_for("administrator.users"))

    sql_do.query(
        FlMembership
    ).filter(
        FlMembership.user_id == user_id
    ).delete()

    sql_do.delete(query_delete_user)
    sql_do.commit()
    return redirect(url_for("administrator.users"))
