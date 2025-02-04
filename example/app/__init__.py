from app.extensions import imp, db
from flask import Flask
from flask_imp.config import ImpConfig, FlaskConfig, DatabaseConfig

flask_config = FlaskConfig(
    secret_key="30c52be45906c36d57f73081f4996a0c0dec32115510aaab",
    additional={
        "test2": "Hello, World!",
    },
)
flask_config.set_additional(
    test="Hello, World!",
)


def create_app():
    app = Flask(__name__, static_url_path="/")
    flask_config.init_app(app)

    imp.init_app(
        app,
        ImpConfig(
            init_session={"logged_in": False},
            database_main=DatabaseConfig(enabled=True, dialect="sqlite"),
        ),
    )

    imp.import_app_resources()
    imp.import_blueprints("blueprints")
    imp.import_models("models")

    # example of imp.register_imp_blueprint
    def self_register_blueprint():
        from app.self_reg import bp as self_reg_bp

        imp.register_imp_blueprint(self_reg_bp)

    self_register_blueprint()

    db.init_app(app)

    print(app.config["TEST"])
    print(app.config["TEST2"])

    with app.app_context():
        db.create_all()

    return app
