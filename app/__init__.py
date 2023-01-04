import os
import secrets

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_bigapp import Auth
from flask_bigapp import BigApp

bigapp = BigApp()
db = SQLAlchemy()

os.environ["CONFIG_SECRET_KEY"] = secrets.token_urlsafe(128)


def create_app():
    app = Flask(__name__)
    bigapp.init_app(app)
    db.init_app(app)

    bigapp.import_builtins()
    bigapp.import_blueprint("www")
    bigapp.import_blueprint("tests")
    bigapp.import_theme("theme")

    bigapp.import_models(from_folder="models")

    @app.before_request
    def before_request():
        bigapp.init_session()

    with app.app_context():
        """
        The following creates all tables from the model files and populates the database
        with test data.
        """
        db.create_all()

        m_example_user = bigapp.model("ExampleUser")
        m_example_table = bigapp.model("ExampleTable")

        if not m_example_user.get_by_id(1):
            salt = Auth.generate_salt()
            gen_password = Auth.generate_password("animals")
            password = Auth.sha_password(gen_password, salt)

            new_example_user = m_example_user(
                username="David",
                password=password,
                salt=salt,
                private_key=Auth.generate_private_key(salt),
                disabled=False
            )
            db.session.add(new_example_user)
            db.session.flush()
            new_example_user_rel = m_example_table(
                user_id=new_example_user.user_id,
                thing=gen_password
            )
            db.session.add(new_example_user_rel)
            db.session.commit()

    return app
