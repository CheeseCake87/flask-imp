from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_sqlalchemy import SQLAlchemy

from .. import FlUser
from .. import FlGroup
from .. import FlMembership
from .. import FlSystemSettings
from .. import bp
from .. import sql_do
from .. import struc
from ....builtins.functions.auth import generate_private_key
from ....builtins.functions.auth import generate_salt
from ....builtins.functions.auth import safe_username
from ....builtins.functions.auth import sha_password
from ....builtins.functions.database import get_tables
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from ....builtins.functions.utilities import string_to_bool
from ....builtins.functions.utilities import is_string_bool
from ....builtins.functions.import_mgr import read_config_as_dict

app_config = read_config_as_dict(app_config=True)


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
        add_system_group = FlGroup(
            group_name="system",
            group_type="system"
        )
        add_user_group = FlGroup(
            group_name="user",
            group_type="system"
        )
        add_administrator_group = FlGroup(
            group_name="administrator",
            group_type="system"
        )
        add_assets_group = FlGroup(
            group_name="assets",
            group_type="system"
        )

        sql_do.add(add_user)
        sql_do.add(add_system_group)
        sql_do.add(add_user_group)
        sql_do.add(add_administrator_group)
        sql_do.add(add_assets_group)

        sql_do.flush()

        add_system_group_membership = FlMembership(
            user_id=add_user.user_id,
            group_id=add_system_group.group_id
        )
        add_user_group_membership = FlMembership(
            user_id=add_user.user_id,
            group_id=add_user_group.group_id
        )
        add_administrator_group_membership = FlMembership(
            user_id=add_user.user_id,
            group_id=add_administrator_group.group_id
        )
        add_assets_group_membership = FlMembership(
            user_id=add_user.user_id,
            group_id=add_assets_group.group_id
        )
        system_setup = FlSystemSettings(
            setup=True
        )

        sql_do.add(add_system_group_membership)
        sql_do.add(add_user_group_membership)
        sql_do.add(add_administrator_group_membership)
        sql_do.add(add_assets_group_membership)
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
