from app import bapp
from .. import bp


@bp.route("/create-all-models", methods=["GET"])
def create_all_models():
    """
    Example of flask_launchpads ability to create all models
    """
    bapp.create_all_models()
    return """If you didn't see an error, this probably worked..."""


@bp.route("/database-example", methods=["GET"])
def database_example():
    # Load the ExampleUser class found in the models folder, this way saves having to import files
    example_user = bapp.model_class("ExampleUser")

    user_id = 1
    result = "NULL"

    find_username = True

    # Query class using sql_do session
    q_example_user = bapp.sql_do.query(example_user)

    if find_username:
        q_example_user = q_example_user.filter(example_user.user_id == user_id)
        if q_example_user.first() is not None:
            username = q_example_user.username
            result = result + f"Username is {username}"

    return f"{result}"
