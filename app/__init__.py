from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_bigapp import Auth
from flask_bigapp import BigApp

bigapp = BigApp()
db = SQLAlchemy()


def create_app():
    main = Flask(__name__)
    bigapp.init_app(main)
    db.init_app(main)

    bigapp.import_structures("structures")
    bigapp.import_models(folder="models")
    bigapp.import_builtins("flask/routes")
    bigapp.import_builtins("flask/template_filters")
    bigapp.import_blueprints("blueprints")

    @main.before_request
    def before_request():
        bigapp.init_session()

    @main.after_request
    def after_request(response):
        return response

    with main.app_context():
        """
        The following creates all tables from the model files and populates the database
        with test data.
        """
        db.create_all()

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
            db.session.add(new_example_user)
            db.session.flush()
            new_example_user_rel = m_example_table(
                user_id=new_example_user.user_id,
                thing=gen_password
            )
            db.session.add(new_example_user_rel)
            db.session.commit()

    """
    This prints all the available routes in the app
    """
    for _ in main.url_map.iter_rules():
        print(_)

    print(bigapp.model_classes)

    return main
