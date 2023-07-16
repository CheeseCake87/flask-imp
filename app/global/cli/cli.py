def collection(app: object):
    @app.cli.command("add-example-user")
    def add_example_user():
        from app.models.example__table import ExampleUserTable

        ExampleUserTable.add(
            username="admin",
            password="password",
            disabled=False,
        )

    @app.cli.command("update-example-user")
    def update_example_user():
        from app.models.example__table import ExampleUserTable

        ExampleUserTable.update(
            user_id=1,
            username="admin-updated",
            private_key="private_key",
            disabled=False,
        )

    @app.cli.command("delete-example-user")
    def delete_example_user():
        from app.models.example__table import ExampleUserTable

        ExampleUserTable.delete(
            user_id=1,
        )
