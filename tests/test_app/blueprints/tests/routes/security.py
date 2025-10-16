import functools

from flask import render_template, session

from flask_imp import ImpBlueprint
from flask_imp.security import checkpoint_callable, checkpoint, SessionCheckpoint
from flask_imp.utilities import lazy_url_for


def include(bp: ImpBlueprint):
    def group_routes(rule, **options):
        def decorator(func):
            @functools.wraps(func)
            @bp.route(rule, **options)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @group_routes("/grouped-decorators", methods=["GET"])
    def grouped_decorators():
        return f"{session.get('logged_in')}"

    @bp.route("/login/bool", methods=["GET"])
    def login_bool():
        session["logged_in"] = True
        return render_template(bp.tmpl("security.html"), logged_in=True)

    @bp.route("/login/str", methods=["GET"])
    def login_str():
        session["logged_in"] = "li"
        return render_template(bp.tmpl("security.html"), logged_in=True)

    @bp.route("/login/int", methods=["GET"])
    def login_int():
        session["logged_in"] = 1
        return render_template(bp.tmpl("security.html"), logged_in=True)

    @bp.route("/logout", methods=["GET"])
    def logout():
        if session.get("logged_in"):
            del session["logged_in"]
        return render_template(bp.tmpl("security.html"), logged_in=False)

    @bp.route("/set-permission/list", methods=["GET"])
    def set_permissions_list():
        session["permissions"] = ["admin"]
        return render_template(bp.tmpl("security.html"), permissions=["admin"])

    @bp.route("/set-permission/value", methods=["GET"])
    def set_permissions_value():
        session["permissions"] = "admin"
        return render_template(bp.tmpl("security.html"), permission="admin")

    @bp.route("/already-logged-in/bool/with-flash", methods=["GET"])
    @checkpoint(
        SessionCheckpoint(
            "logged_in",
            True,
        ).action(
            pass_url=lazy_url_for("tests.already_logged_in"),
            message="Already logged in",
        )
    )
    def already_logged_in_bool():
        return render_template(
            bp.tmpl("security.html"), logged_in_on=session.get("logged_in")
        )

    @bp.route("/must-be-logged-in/bool", methods=["GET"])
    @checkpoint(
        SessionCheckpoint(
            "logged_in", True
        ).action(lazy_url_for("tests.login_failed"))
    )
    def must_be_logged_in_bool():
        return render_template(bp.tmpl("security.html"), logged_in_on=True)

    @bp.route("/must-be-logged-in/bool/with-flash", methods=["GET"])
    @checkpoint(SessionCheckpoint(
        "logged_in", True
    ).action(
        lazy_url_for("tests.login_failed"),
        message="Login needed"
    ))
    def must_be_logged_in_bool_with_flash():
        return render_template(bp.tmpl("security.html"), logged_in_on=True)

    @bp.route("/must-be-logged-in/str", methods=["GET"])
    @checkpoint(
        SessionCheckpoint(
            "logged_in", "li"
        ).action(
            lazy_url_for("tests.login_failed"))
    )
    def must_be_logged_in_str():
        return render_template(bp.tmpl("security.html"), logged_in_on="li")

    @bp.route("/must-be-logged-in/int", methods=["GET"])
    @checkpoint(
        SessionCheckpoint(
            "logged_in", 1
        ).action(
            lazy_url_for("tests.login_failed")
        )
    )
    def must_be_logged_in_int():
        return render_template(bp.tmpl("security.html"), logged_in_on=1)

    @bp.route("/must-be-logged-in/multi", methods=["GET"])
    @checkpoint(
        SessionCheckpoint(
            "logged_in", [1, "li", True]
        ).action(
            lazy_url_for("tests.login_failed")
        )
    )
    def must_be_logged_in_multi():
        return render_template(
            bp.tmpl("security.html"), logged_in_on=session.get("logged_in")
        )

    @bp.route("/must-have-permissions/std", methods=["GET"])
    @checkpoint(
        SessionCheckpoint(
            "permissions", ["admin", "manager"]
        ).action(
            lazy_url_for("tests.permission_failed")
        )
    )
    def permission_check_std():
        return render_template(bp.tmpl("security.html"))

    @bp.route("/must-have-permissions/adv", methods=["GET"])
    @checkpoint(
        SessionCheckpoint(
            "permissions", ["super-admin"]
        ).action(
            lazy_url_for("tests.permission_failed")
        )
    )
    def permission_check_adv():
        return render_template(bp.tmpl("security.html"))

    # def check_if_number(number, __url_vars__=None):
    #     try:
    #         int(number)
    #         return True
    #     except ValueError:
    #         return False
    #
    # @bp.route("/pass-func-check", methods=["GET"])
    # @checkpoint_callable(check_if_number,
    #                      fail_url=lazy_url_for("tests.permission_failed"))
    # def pass_function_check_std():
    #     return "Pass"
    #
    # @bp.route("/pass-func-check-with-url-var-replaced/<number>", methods=["GET"])
    # @checkpoint_callable(check_if_number, {"number": 10}, "tests.permission_failed")
    # def pass_function_check_with_url_value(number):
    #     # Expecting to pass with response: URL value: <number>
    #     return f"URL value: {number}"
    #
    # @bp.route(
    #     "/pass-func-check-with-url-var-replaced-and-app-context/<number>",
    #     methods=["GET"]
    # )
    # @checkpoint_callable(
    #     check_if_number,
    #     {"number": 10},
    #     "tests.permission_failed",
    # )
    # def pass_function_check_with_url_value_with_ac(number):
    #     # Expecting to pass with response: URL value: <number>
    #     return f"URL value: {number}"
    #
    # @bp.route(
    #     "/pass-func-check-with-url-var-replaced-and-app-context-with-partial/<number>",
    #     methods=["GET"],
    # )
    # @checkpoint_callable(
    #     check_if_number,
    #     {"number": 10},
    #     "tests.permission_failed",
    # )
    # def pass_function_check_with_url_value_with_ac_with_partial(number):
    #     # Expecting to pass with response: URL value: <number>
    #     return f"URL value: {number}"

    @bp.route("/login-failed", methods=["GET"])
    def login_failed():
        return render_template(bp.tmpl("login_failed.html"))

    @bp.route("/already-logged-in", methods=["GET"])
    def already_logged_in():
        return render_template(bp.tmpl("already_logged_in.html"))

    @bp.route("/permission-failed", methods=["GET"])
    def permission_failed():
        return "Permission failed"
