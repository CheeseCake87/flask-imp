from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_bigapp import BigApp
from flask_bigapp import Auth

bigapp = BigApp()
db = SQLAlchemy()


def create_app():
    main = Flask(__name__)
    bigapp.init_app(main, db)
    bigapp.import_structures("structures")
    bigapp.import_models(folder="models")
    bigapp.import_builtins("flask/routes")
    bigapp.import_builtins("flask/template_filters")
    bigapp.import_blueprints("blueprints")

    with main.app_context():
        """
        The following creates all tables from the model files and populates the database
        with test data.
        """
        bigapp.db.create_all()

        m_example_user = bigapp.model_class("ExampleUser")
        m_example_table = bigapp.model_class("ExampleTable")

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
            bigapp.sql_do.add(new_example_user)
            bigapp.sql_do.flush()
            new_example_user_rel = m_example_table(
                user_id=new_example_user.user_id,
                thing=gen_password
            )
            bigapp.sql_do.add(new_example_user_rel)
            bigapp.sql_do.commit()

    """
    This prints all the available routes in the app
    """
    for _ in main.url_map.iter_rules():
        print(_)

    return main
