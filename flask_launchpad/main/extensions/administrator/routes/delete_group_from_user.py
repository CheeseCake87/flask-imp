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


@bp.route("/users/edit/<user_id>/delete/group/<group_id>", methods=["GET"])
def delete_group_from_user(user_id, group_id):
    sql_do.query(
        FlMembership
    ).filter(
        FlMembership.group_id == group_id,
        FlMembership.user_id == user_id
    ).delete()
    sql_do.commit()
    return redirect(url_for("administrator.edit_user", user_id=user_id))
