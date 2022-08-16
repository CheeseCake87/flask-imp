from app._flask_bigapp.src.flask_bigapp import Auth
from flask import render_template

from app import bigapp
from app.blueprints.example import bp


@bp.route("/auth-example", methods=["GET"])
def auth_example():


    examples = dict()

    examples.update({
        "Auth.is_username_safe('&HEOI_')": Auth.is_username_safe("&HEOI_")
    })
    examples.update({
        "Auth.is_username_safe('email@email.com')": Auth.is_username_safe('email@email.com')
    })
    examples.update({
        "Auth.is_username_safe('email@email@email.com')": Auth.is_username_safe('email@email@email.com')
    })
    examples.update({
        "Info": "Special characters are not allow in usernames, but email addresses are allowed: @ . - _ "
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

    render = bp.render("auth-example.html")
    extend = bigapp.extend("bigapp_default", "main.html")
    footer = bigapp.include("bigapp_default", "footer.html")

    return render_template(render, extend=extend, footer=footer, examples=examples)