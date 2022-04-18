from flask import redirect
from flask import session
from flask import url_for
from sqlalchemy.orm.exc import NoResultFound

from .. import FlGroup
from .. import FlMembership
from .. import bp
from .. import sql_do
from ....builtins.functions.security import login_required


@bp.route("/groups/delete/<group_id>", methods=["GET"])
@login_required("auth", "account.login")
def delete_group(group_id):
    try:
        query_delete_group = sql_do.query(
            FlGroup
        ).filter(
            FlGroup.group_id == group_id
        ).first()
    except NoResultFound:
        session["error"] = f"No group found using the group_id {group_id}"
        return redirect(url_for("administrator.groups"))

    if query_delete_group is None:
        session["error"] = f"No group found using the group_id {group_id}"
        return redirect(url_for("administrator.groups"))

    sql_do.query(
        FlMembership
    ).filter(
        FlMembership.group_id == group_id
    ).delete()

    sql_do.delete(query_delete_group)
    sql_do.commit()
    return redirect(url_for("administrator.groups"))
