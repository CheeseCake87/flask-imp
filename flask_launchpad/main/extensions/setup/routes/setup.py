from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_sqlalchemy import SQLAlchemy

from ....builtins.functions.auth import generate_private_key
from ....builtins.functions.auth import generate_salt
from ....builtins.functions.auth import safe_username
from ....builtins.functions.auth import sha_password
from ....builtins.functions.database import get_tables
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from ....builtins.functions.import_mgr import read_config_as_dict

from .. import FlUser
from .. import FlPermission
from .. import FlPermissionMembership
from .. import FlCompany
from .. import FlCompanyMembership
from .. import FlTeam
from .. import FlTeamMembership
from .. import FlSystemSettings
from .. import bp
from .. import sql_do
from .. import struc

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

        # Add user
        salt = generate_salt()
        private_key = generate_private_key(salt)
        add_user = FlUser(
            username=request.form["username"].lower(),
            password=sha_password(request.form["password"], salt),
            salt=salt,
            private_key=private_key,
            disabled=False
        )

        # Add system company
        add_system_company = FlCompany(
            name="__system__",
        )

        # Add system team
        add_system_team = FlTeam(
            name="__system__",
        )

        # Add permission groups
        add_system_perm = FlPermission(
            name="system",
            type="system"
        )
        add_user_perm = FlPermission(
            name="user",
            type="system"
        )
        add_administrator_perm = FlPermission(
            name="administrator",
            type="system"
        )
        add_assets_perm = FlPermission(
            name="assets",
            type="system"
        )

        # Insert into database session and flush to get IDs
        sql_do.add(add_system_company)
        sql_do.add(add_system_team)
        sql_do.add(add_user)
        sql_do.add(add_system_perm)
        sql_do.add(add_user_perm)
        sql_do.add(add_administrator_perm)
        sql_do.add(add_assets_perm)
        sql_do.flush()

        # Add user to company
        add_to_system_company = FlCompanyMembership(
            user_id=add_user.user_id,
            company_id=add_system_company.company_id
        )

        # Add user to team
        add_to_system_team = FlTeamMembership(
            user_id=add_user.user_id,
            team_id=add_system_team.team_id
        )

        # Add user to permission groups
        add_system_perm_mem = FlPermissionMembership(
            user_id=add_user.user_id,
            permission_id=add_system_perm.permission_id
        )
        add_user_perm_mem = FlPermissionMembership(
            user_id=add_user.user_id,
            permission_id=add_user_perm.permission_id
        )
        add_administrator_perm_mem = FlPermissionMembership(
            user_id=add_user.user_id,
            permission_id=add_administrator_perm.permission_id
        )
        add_assets_perm_mem = FlPermissionMembership(
            user_id=add_user.user_id,
            permission_id=add_assets_perm.permission_id
        )

        # Mark system as being setup
        system_setup = FlSystemSettings(
            setup=True
        )

        # Insert into database session
        sql_do.add(add_to_system_company)
        sql_do.add(add_to_system_team)

        sql_do.add(add_system_perm_mem)
        sql_do.add(add_user_perm_mem)
        sql_do.add(add_administrator_perm_mem)
        sql_do.add(add_assets_perm_mem)

        sql_do.add(system_setup)

        # Commit to database
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
