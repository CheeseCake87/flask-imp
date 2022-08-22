from flask import render_template

from app import bigapp
from .. import bp, page_needs


@bp.route("/create-all-models", methods=["GET"])
def create_all_models():
    """
    Creates database based on the models file
    """
    bigapp.create_all_models()
    return """If you didn't see an error, this probably worked..."""


@bp.route("/database-example", methods=["GET"])
def database_example():
    # Load the ExampleUser class found in the import_models folder, this way saves having to import files
    example_user = bigapp.model_class("ExampleUser")

    user_id = 1
    result = "NULL"
    find_username = True

    # Normal query
    nq_example_user = example_user.query

    # Query class using sql_do session
    sq_example_user = bigapp.sql_do.query(example_user)

    if find_username:
        sq_example_user = sq_example_user.filter(example_user.user_id == user_id).first()
        if sq_example_user is not None:
            username = sq_example_user.username
            result = f"Session Query: Username is {username}"

        nq_example_user = nq_example_user.filter(example_user.user_id == user_id).first()
        if nq_example_user is not None:
            username = nq_example_user.username
            example_table_join = nq_example_user.rel_example_table[0].thing
            result = f"{result}, Normal Query: Username is {username} -> ExampleTable Join: {example_table_join}"

    render = bp.tmpl("database-example.html")
    return render_template(render, result=result, **page_needs)
