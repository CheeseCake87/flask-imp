from flask_bigapp import Auth
from flask import render_template

from .. import bp, page_needs


@bp.route("/auth-example", methods=["GET"])
def auth_example():


    examples = dict()

    examples.update({
        "Auth.is_username_valid('&HEOI_')": Auth.is_username_valid("&HEOI_")
    })
    examples.update({
        "Auth.is_email_address_valid('email@email.com')": Auth.is_email_address_valid('email@email.com')
    })
    examples.update({
        "Auth.is_email_address_valid('email@email@email.com')": Auth.is_email_address_valid('email@email@email.com')
    })
    examples.update({
        "Info": "Usernames can only contain letters, numbers, ., -, and _ but not begin or end with the last three mentioned."
    })

    examples.update({
        "Auth.generate_email_validator()": Auth.generate_email_validator()
    })

    examples.update({
        "Auth.generate_form_token()": Auth.generate_form_token()
    })

    examples.update({
        "Auth.generate_salt()": Auth.generate_salt()
    })

    examples.update({
        "Auth.generate_pepper('password')": Auth.generate_pepper("password")
    })

    examples.update({
        "Auth.generate_password(style='animals', length=2)": Auth.generate_password(style="animals", length=2)
    })
    password = Auth.generate_password(style="animals", length=2)
    salt = Auth.generate_salt()
    examples.update({
        "Auth.sha_password(password, salt, encrypt=128)": Auth.sha_password(password, salt, encrypt=128)
    })

    render = bp.tmpl("auth-example.html")
    return render_template(render, examples=examples, **page_needs)
