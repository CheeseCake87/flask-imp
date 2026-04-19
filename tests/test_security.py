"""
Tests for src/flask_imp/security.

Builds a minimal Flask app with routes that exercise each checkpoint surface
independently from the main `test_app` fixture used by test_group.py.
"""

import base64

import pytest
from flask import Flask, jsonify, make_response, session

from flask_imp.security import (
    APIKeyCheckpoint,
    BaseCheckpoint,
    BearerCheckpoint,
    SessionCheckpoint,
    checkpoint,
    checkpoint_callable,
    include_csrf,
)
from flask_imp.utilities import lazy_session_get, lazy_url_for


API_KEY = "secret-header-key"
BEARER_TOKEN = "secret-bearer-token"


def _build_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "test-secret"
    app.config.update(TESTING=True)

    # ------------------------------------------------------------------
    # Bare landing pages used as redirect targets.
    # ------------------------------------------------------------------
    @app.route("/fail-page")
    def fail_page():
        return "failed", 200

    @app.route("/pass-page")
    def pass_page():
        return "passed", 200

    @app.route("/index")
    def index():
        return "index", 200

    # ------------------------------------------------------------------
    # SessionCheckpoint — covers single value, list values, and each
    # .action() branch: default abort, fail_url, fail_json, fail_response,
    # pass_url, disable_default_fail.
    # ------------------------------------------------------------------
    @app.route("/session/login")
    def session_login():
        session["logged_in"] = True
        return "logged in", 200

    @app.route("/session/logout")
    def session_logout():
        session.clear()
        return "logged out", 200

    @app.route("/session/set-role/<role>")
    def session_set_role(role: str):
        session["role"] = role
        return f"role set to {role}", 200

    LOGGED_IN = SessionCheckpoint("logged_in", True).action()

    @app.route("/session/protected-default")
    @checkpoint(LOGGED_IN)
    def session_protected_default():
        return "ok", 200

    LOGGED_IN_FAIL_URL = SessionCheckpoint("logged_in", True).action(
        fail_url="/fail-page", message="need login"
    )

    @app.route("/session/protected-fail-url")
    @checkpoint(LOGGED_IN_FAIL_URL)
    def session_protected_fail_url():
        return "ok", 200

    LOGGED_IN_FAIL_JSON = SessionCheckpoint("logged_in", True).action(
        fail_json={"error": "login required"}, fail_status=401
    )

    @app.route("/session/protected-fail-json")
    @checkpoint(LOGGED_IN_FAIL_JSON)
    def session_protected_fail_json():
        return jsonify(ok=True)

    LOGGED_IN_FAIL_RESPONSE = SessionCheckpoint("logged_in", True).action(
        fail_response=lambda: make_response("custom fail", 418)
    )

    @app.route("/session/protected-fail-response")
    @checkpoint(LOGGED_IN_FAIL_RESPONSE)
    def session_protected_fail_response():
        return "ok", 200

    ALREADY_IN = SessionCheckpoint("logged_in", True).action(pass_url="/pass-page")

    @app.route("/session/login-page")
    @checkpoint(ALREADY_IN)
    def session_login_page():
        return "login form", 200

    LOGGED_IN_DISABLE_DEFAULT = SessionCheckpoint("logged_in", True).action(
        disable_default_fail=True
    )

    @app.route("/session/protected-disable-default")
    @checkpoint(LOGGED_IN_DISABLE_DEFAULT)
    def session_protected_disable_default():
        return "fell through", 200

    ROLE_IN_LIST = SessionCheckpoint("role", ["admin", "editor"]).action(
        fail_status=403
    )

    @app.route("/session/role-list")
    @checkpoint(ROLE_IN_LIST)
    def session_role_list():
        return "ok", 200

    LAZY_FAIL = SessionCheckpoint("logged_in", True).action(
        fail_url=lazy_url_for("index")
    )

    @app.route("/session/lazy-fail")
    @checkpoint(LAZY_FAIL)
    def session_lazy_fail():
        return "ok", 200

    # ------------------------------------------------------------------
    # APIKeyCheckpoint — header + query_param.
    # ------------------------------------------------------------------
    HEADER_KEY = APIKeyCheckpoint(API_KEY, type_="header").action(
        fail_json={"error": "bad key"}, fail_status=401
    )

    @app.route("/api/header")
    @checkpoint(HEADER_KEY)
    def api_header():
        return jsonify(ok=True)

    QUERY_KEY = APIKeyCheckpoint(API_KEY, type_="query_param", header_or_param="api_key").action(
        fail_json={"error": "bad key"}, fail_status=401
    )

    @app.route("/api/query")
    @checkpoint(QUERY_KEY)
    def api_query():
        return jsonify(ok=True)

    # ------------------------------------------------------------------
    # BearerCheckpoint — exercises secrets.compare_digest path.
    # ------------------------------------------------------------------
    BEARER = BearerCheckpoint(BEARER_TOKEN).action(
        fail_json={"error": "bad token"}, fail_status=401
    )

    @app.route("/api/bearer")
    @checkpoint(BEARER)
    def api_bearer():
        return jsonify(ok=True)

    # ------------------------------------------------------------------
    # checkpoint_callable — pass/fail plus each action.
    # ------------------------------------------------------------------
    def always_true(**_kwargs):
        return True

    def always_false(**_kwargs):
        return False

    def session_has_flag(**kwargs):
        return kwargs.get("value") is True

    def url_arg_is_admin(**kwargs):
        url_vars = kwargs.get("__url_vars__") or {}
        return url_vars.get("name") == "admin"

    @app.route("/callable/pass")
    @checkpoint_callable(always_true)
    def callable_pass():
        return "ok", 200

    @app.route("/callable/fail-url")
    @checkpoint_callable(always_false, fail_url="/fail-page")
    def callable_fail_url():
        return "ok", 200

    @app.route("/callable/fail-json")
    @checkpoint_callable(always_false, fail_json={"error": "no"}, fail_status=401)
    def callable_fail_json():
        return "ok", 200

    @app.route("/callable/fail-response")
    @checkpoint_callable(
        always_false, fail_response=lambda: make_response("teapot", 418)
    )
    def callable_fail_response():
        return "ok", 200

    @app.route("/callable/pass-url")
    @checkpoint_callable(always_true, pass_url="/pass-page")
    def callable_pass_url():
        return "ok", 200

    @app.route("/callable/disable-default-fail")
    @checkpoint_callable(always_false, disable_default_fail=True)
    def callable_disable_default_fail():
        return "fell through", 200

    @app.route("/callable/default-fail")
    @checkpoint_callable(always_false, fail_status=403)
    def callable_default_fail():
        return "ok", 200

    @app.route("/callable/lazy-session")
    @checkpoint_callable(
        session_has_flag,
        predefined_args={"value": lazy_session_get("flag", False)},
        fail_status=403,
    )
    def callable_lazy_session():
        return "ok", 200

    @app.route("/callable/url-args/<name>")
    @checkpoint_callable(url_arg_is_admin, include_url_args=True, fail_status=403)
    def callable_url_args(name: str):
        return f"hello {name}", 200

    # ------------------------------------------------------------------
    # include_csrf
    # ------------------------------------------------------------------
    @app.route("/csrf-form", methods=["GET", "POST"])
    @include_csrf(session_key="csrf", form_key="csrf")
    def csrf_form():
        if "csrf" in session:
            return session["csrf"], 200
        return "no token", 200

    # ------------------------------------------------------------------
    # `checkpoint` rejects anything that isn't a BaseCheckpoint.
    # ------------------------------------------------------------------
    @app.route("/bad-checkpoint")
    @checkpoint("not a checkpoint")  # type: ignore[arg-type]
    def bad_checkpoint():
        return "ok", 200

    return app


@pytest.fixture(scope="module")
def sec_app():
    return _build_app()


@pytest.fixture()
def sec_client(sec_app):
    return sec_app.test_client()


# ---------------------------------------------------------------------------
# SessionCheckpoint
# ---------------------------------------------------------------------------
def test_session_checkpoint_pass(sec_client):
    sec_client.get("/session/login")
    assert sec_client.get("/session/protected-default").status_code == 200


def test_session_checkpoint_default_aborts_when_not_logged_in(sec_client):
    sec_client.get("/session/logout")
    assert sec_client.get("/session/protected-default").status_code == 403


def test_session_checkpoint_fail_url_redirects(sec_client):
    sec_client.get("/session/logout")
    response = sec_client.get("/session/protected-fail-url")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/fail-page")


def test_session_checkpoint_fail_json_returned(sec_client):
    sec_client.get("/session/logout")
    response = sec_client.get("/session/protected-fail-json")
    assert response.status_code == 401
    assert response.get_json() == {"error": "login required"}


def test_session_checkpoint_fail_response_returned(sec_client):
    sec_client.get("/session/logout")
    response = sec_client.get("/session/protected-fail-response")
    assert response.status_code == 418
    assert response.data == b"custom fail"


def test_session_checkpoint_pass_url_redirects(sec_client):
    sec_client.get("/session/login")
    response = sec_client.get("/session/login-page")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/pass-page")


def test_session_checkpoint_disable_default_fail_runs_view(sec_client):
    sec_client.get("/session/logout")
    response = sec_client.get("/session/protected-disable-default")
    assert response.status_code == 200
    assert response.data == b"fell through"


def test_session_checkpoint_list_values_match(sec_client):
    sec_client.get("/session/set-role/admin")
    assert sec_client.get("/session/role-list").status_code == 200

    sec_client.get("/session/set-role/guest")
    assert sec_client.get("/session/role-list").status_code == 403


def test_session_checkpoint_lazy_url_for(sec_client):
    sec_client.get("/session/logout")
    response = sec_client.get("/session/lazy-fail")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/index")


# ---------------------------------------------------------------------------
# APIKeyCheckpoint
# ---------------------------------------------------------------------------
def test_api_key_header_pass(sec_client):
    response = sec_client.get("/api/header", headers={"x-api-key": API_KEY})
    assert response.status_code == 200


def test_api_key_header_fail_missing(sec_client):
    response = sec_client.get("/api/header")
    assert response.status_code == 401
    assert response.get_json() == {"error": "bad key"}


def test_api_key_header_fail_wrong(sec_client):
    response = sec_client.get("/api/header", headers={"x-api-key": "wrong"})
    assert response.status_code == 401


def test_api_key_query_pass(sec_client):
    response = sec_client.get(f"/api/query?api_key={API_KEY}")
    assert response.status_code == 200


def test_api_key_query_fail(sec_client):
    response = sec_client.get("/api/query?api_key=wrong")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# BearerCheckpoint
# ---------------------------------------------------------------------------
def test_bearer_pass(sec_client):
    response = sec_client.get(
        "/api/bearer", headers={"Authorization": f"Bearer {BEARER_TOKEN}"}
    )
    assert response.status_code == 200


def test_bearer_fail_wrong_token(sec_client):
    response = sec_client.get(
        "/api/bearer", headers={"Authorization": "Bearer nope"}
    )
    assert response.status_code == 401


def test_bearer_fail_missing_auth(sec_client):
    response = sec_client.get("/api/bearer")
    assert response.status_code == 401


def test_bearer_fail_wrong_auth_type(sec_client):
    basic = base64.b64encode(b"user:pass").decode()
    response = sec_client.get(
        "/api/bearer", headers={"Authorization": f"Basic {basic}"}
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# checkpoint_callable
# ---------------------------------------------------------------------------
def test_callable_pass(sec_client):
    assert sec_client.get("/callable/pass").status_code == 200


def test_callable_fail_url(sec_client):
    response = sec_client.get("/callable/fail-url")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/fail-page")


def test_callable_fail_json(sec_client):
    response = sec_client.get("/callable/fail-json")
    assert response.status_code == 401
    assert response.get_json() == {"error": "no"}


def test_callable_fail_response(sec_client):
    response = sec_client.get("/callable/fail-response")
    assert response.status_code == 418
    assert response.data == b"teapot"


def test_callable_pass_url(sec_client):
    response = sec_client.get("/callable/pass-url")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/pass-page")


def test_callable_disable_default_fail_runs_view(sec_client):
    response = sec_client.get("/callable/disable-default-fail")
    assert response.status_code == 200
    assert response.data == b"fell through"


def test_callable_default_fail_aborts(sec_client):
    response = sec_client.get("/callable/default-fail")
    assert response.status_code == 403


def test_callable_lazy_session_pass(sec_client):
    with sec_client.session_transaction() as s:
        s["flag"] = True
    assert sec_client.get("/callable/lazy-session").status_code == 200


def test_callable_lazy_session_fail(sec_client):
    with sec_client.session_transaction() as s:
        s.pop("flag", None)
    assert sec_client.get("/callable/lazy-session").status_code == 403


def test_callable_include_url_args_pass(sec_client):
    assert sec_client.get("/callable/url-args/admin").status_code == 200


def test_callable_include_url_args_fail(sec_client):
    assert sec_client.get("/callable/url-args/guest").status_code == 403


# ---------------------------------------------------------------------------
# include_csrf
# ---------------------------------------------------------------------------
def test_csrf_get_sets_token(sec_client):
    response = sec_client.get("/csrf-form")
    assert response.status_code == 200
    assert response.data  # token echoed back


def test_csrf_post_valid_token_passes(sec_client):
    token = sec_client.get("/csrf-form").data.decode()
    response = sec_client.post("/csrf-form", data={"csrf": token})
    assert response.status_code == 200


def test_csrf_post_mismatched_token_aborts(sec_client):
    sec_client.get("/csrf-form")
    response = sec_client.post("/csrf-form", data={"csrf": "wrong"})
    assert response.status_code == 401


def test_csrf_post_missing_form_key_aborts(sec_client):
    sec_client.get("/csrf-form")
    response = sec_client.post("/csrf-form", data={})
    assert response.status_code == 401


def test_csrf_post_missing_session_key_aborts(sec_client):
    # Fresh client with no prior GET — no session token established.
    fresh = sec_client.application.test_client()
    response = fresh.post("/csrf-form", data={"csrf": "anything"})
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Misuse / type guard on the `checkpoint` decorator.
# ---------------------------------------------------------------------------
def test_checkpoint_rejects_non_checkpoint(sec_client):
    with pytest.raises(TypeError):
        sec_client.get("/bad-checkpoint")


# ---------------------------------------------------------------------------
# BaseCheckpoint itself is not meant to be used directly.
# ---------------------------------------------------------------------------
def test_base_checkpoint_pass_is_abstract():
    with pytest.raises(NotImplementedError):
        BaseCheckpoint().pass_()