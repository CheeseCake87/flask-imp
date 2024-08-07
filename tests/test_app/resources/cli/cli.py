from importlib import import_module

from flask import Flask


def collection(app: Flask):
    @app.cli.command("add-example-user")
    def add_example_user():
        from ...models.example_table import ExampleTable

        ExampleTable.add(
            username="admin",
            password="password",
            disabled=False,
        )

    @app.cli.command("update-example-user")
    def update_example_user():
        from ...models.example_table import ExampleTable

        ExampleTable.update(
            user_id=1,
            username="admin-updated",
            private_key="private_key",
            disabled=False,
        )

    @app.cli.command("delete-example-user")
    def delete_example_user():
        from ...models.example_table import ExampleTable

        ExampleTable.delete(
            user_id=1,
        )

    @app.cli.command("example-model-function")
    def example_model_function():
        from ...extensions import imp

        imp.import_models("models")

        example_table_meta = imp.model_meta("ExampleTable")
        users_module = import_module(example_table_meta["location"])
        users_module.example_function()
