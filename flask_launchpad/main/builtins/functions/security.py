from hashlib import md5
from functools import wraps
from flask import current_app
from flask import session
from flask import url_for
from flask import redirect
from werkzeug.routing import BuildError


def file_extension_allowed(file_extension: str):
    allowed = ["doc", "docx", "odt", "pdf"]
    if file_extension in allowed:
        return True
    return False


def build_secure_filename(generate_hash_from: str, file_extension: str, label: str = "file") -> str:
    generate_hash = md5()
    generate_hash.update(generate_hash_from.encode("utf-8"))
    filename = generate_hash.hexdigest()
    return f"{label}_{filename}.{file_extension}"


def force_legal_filename(new_filename: str, file_extension: str, label: str = "file") -> str:
    return f"{label}_{new_filename}.{file_extension}"


def generate_secure_folder_name(generate_hash_from: str) -> str:
    generate_hash = md5()
    generate_hash.update(generate_hash_from.encode("utf-8"))
    folder = generate_hash.hexdigest()
    return f"{folder}"


def login_required(session_bool_key: str, on_error_endpoint: str):
    def login_required_wrapper(func):
        @wraps(func)
        def secure_function(*args, **kwargs):

            if on_error_endpoint == "":
                return redirect(url_for("system.redirect_catch_all", message="on_error_endpoint not in args"))

            try:
                url_for(on_error_endpoint)
            except BuildError:
                return redirect(url_for("system.redirect_catch_all", tried=on_error_endpoint))

            if session_bool_key not in session:
                session["error"] = "You need to be logged in to access this page"
                return redirect(url_for(on_error_endpoint))

            if not session[session_bool_key]:
                session["error"] = "You need to be logged in to access this page"
                return redirect(url_for(on_error_endpoint))

            return func(*args, **kwargs)

        return secure_function

    return login_required_wrapper


def logged_in_check(session_bool_key: str, on_true_endpoint: str):
    def logged_in_check_wrapper(func):
        @wraps(func)
        def secure_function(*args, **kwargs):

            if on_true_endpoint == "":
                return redirect(url_for("system.redirect_catch_all", message="on_error_endpoint not in args"))

            try:
                url_for(on_true_endpoint)
            except BuildError:
                return redirect(url_for("system.redirect_catch_all", tried=on_true_endpoint))

            if session_bool_key in session:
                if session[session_bool_key]:
                    return redirect(url_for(on_true_endpoint))

            return func(*args, **kwargs)

        return secure_function

    return logged_in_check_wrapper
