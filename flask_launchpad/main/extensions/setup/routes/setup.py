from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_sqlalchemy import SQLAlchemy

from .. import FlUser
from .. import FlPermissions
from .. import FlPermissionsMembership
from .. import FlClan
from .. import FlClanMembership
from .. import FlTeam
from .. import FlTeamMembership
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

    for key, value in tables.items():
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
        add_system_perm = FlPermissions(
            name="system",
            type="system"
        )
        add_user_perm = FlPermissions(
            name="user",
            type="system"
        )
        add_administrator_perm = FlPermissions(
            name="administrator",
            type="system"
        )
        add_assets_perm = FlPermissions(
            name="assets",
            type="system"
        )

        sql_do.add(add_user)
        sql_do.add(add_system_perm)
        sql_do.add(add_user_perm)
        sql_do.add(add_administrator_perm)
        sql_do.add(add_assets_perm)

        sql_do.flush()

        add_system_perm_mem = FlPermissionsMembership(
            user_id=add_user.user_id,
            permissions_id=add_system_perm.group_id
        )
        add_user_perm_mem = FlPermissionsMembership(
            user_id=add_user.user_id,
            permissions_id=add_user_perm.group_id
        )
        add_administrator_perm_mem = FlPermissionsMembership(
            user_id=add_user.user_id,
            permissions_id=add_administrator_perm.group_id
        )
        add_assets_perm_mem = FlPermissionsMembership(
            user_id=add_user.user_id,
            permissions_id=add_assets_perm.group_id
        )
        system_setup = FlSystemSettings(
            setup=True
        )

        sql_do.add(add_system_perm_mem)
        sql_do.add(add_user_perm_mem)
        sql_do.add(add_administrator_perm_mem)
        sql_do.add(add_assets_perm_mem)
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
