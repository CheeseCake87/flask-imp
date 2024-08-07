from flask import Flask, current_app


@current_app.route("/current-app-import")
def current_app_import():
    return "current_app_import"


def collection(app: Flask):
    @app.route("/collection-factory-import")
    def collection_factory_import():
        return "collection_factory_import"
