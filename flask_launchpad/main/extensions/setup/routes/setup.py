from ....builtins.functions.security import login_required
from ....builtins.functions.auth import sha_password
from ....builtins.functions.auth import generate_salt
from ....builtins.functions.auth import generate_private_key
from ....builtins.functions.auth import safe_username
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from ....builtins.functions.database import get_tables
from .. import bp
from .. import struc
from .. import sql_do
from .. import FlUser
from .. import FlGroup
from .. import FlMembership
from .. import FlSystemSettings
from flask import request
from flask import current_app
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy


@bp.route("/", methods=["GET", "POST"])
def setup():
    error = session["error"]
    message = session["message"]
    render = "renders/setup.html"
    structure = struc.name()
    extend = struc.extend("backend.html")
    footer = struc.include("footer.html")

    tables = get_tables()
    system_modules = ["system", "administrator", "account", "uploads"]

    for key, value in tables.items():
        if key in system_modules:
            SQLAlchemy.create_all(current_app.config["SHARED_MODELS"][key])

    system_setup = sql_do.query(
        FlSystemSettings
    ).filter(
        FlSystemSettings.system_settings_id == 1
    ).first()

    if system_setup is not None:
        session["error"] = "System has already been setup"
        return redirect(url_for("account.login"))

    if request.method == "POST":
        if request.form["password"] != request.form["confirm_password"]:
            session["error"] = "Passwords do not match"
            return redirect(url_for("setup.setup"))
        if not safe_username(request.form["username"]):
            session["error"] = "Username cannot have any special characters"
            return redirect(url_for("setup.setup"))

        salt = generate_salt()
        private_key = generate_private_key(salt)
        add_user = FlUser(
            username=request.form["username"].lower(),
            password=sha_password(request.form["password"], salt),
            salt=salt,
            private_key=private_key,
            disabled=False
        )
        add_group = FlGroup(
            group_type="system",
            group_name="system"
        )
        sql_do.add(add_user)
        sql_do.add(add_group)
        sql_do.flush()
        add_membership = FlMembership(
            user_id=add_user.user_id,
            group_id=add_group.group_id
        )
        sql_do.add(add_membership)
        system_setup = FlSystemSettings(
            setup=True
        )
        sql_do.add(system_setup)
        sql_do.commit()

        return redirect(url_for("account.login"))

    return render_template(
        render,
        structure=structure,
        extend=extend,
        footer=footer,
        error=error,
        clear_error=clear_error(),
        message=message,
        clear_message=clear_message()
    )
