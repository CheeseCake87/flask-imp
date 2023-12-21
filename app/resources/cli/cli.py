from flask import current_app as app
from app.extensions import db
from app.models.example_user_table import ExampleUserTable


@app.cli.command("config")
def create_tables():
    print(app.config)


@app.cli.command("create-tables")
def create_tables():
    db.create_all()


@app.cli.command("get-example-user")
def get_example_user():
    result = ExampleUserTable.get_by_id(1)
    if not result:
        print("User not found.")
        return
    print(
        f"""
        user_id: {result.user_id}
        username: {result.username}
        salt: {result.salt}
        password: {result.password}
        private_key: {result.private_key}
        disabled: {result.disabled}
        """
    )


@app.cli.command("create-example-user")
def add_example_user():
    ExampleUserTable.create(
        username="admin",
        password="password",
        disabled=False,
    )


@app.cli.command("update-example-user")
def update_example_user():
    ExampleUserTable.update(
        user_id=1,
        username="admin-updated",
        private_key="private_key",
        disabled=False,
    )


@app.cli.command("delete-example-user")
def delete_example_user():
    ExampleUserTable.delete(
        user_id=1,
    )
