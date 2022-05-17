from flask import render_template
from flask import session

from ....builtins.functions.security import login_required
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message

from .. import bp
from .. import struc


@bp.route("/dashboard", methods=["GET"])
@login_required("auth", "account.login")
def dashboard():
    from ....builtins.functions.memberships import get_permission_membership_from_user_id

    error = session["error"]
    message = session["message"]
    render = "renders/dashboard.html"
    structure = struc.name()
    extend = struc.extend("backend.html")
    footer = struc.include("footer.html")

    return render_template(
        render,
        structure=structure,
        extend=extend,
        footer=footer,
        error=error,
        clear_error=clear_error(),
        message=message,
        clear_message=clear_message(),
        user_permissions=get_permission_membership_from_user_id(session["user_id"])
    )
