from flask import Flask


def collection(app: Flask):
    @app.route("/collection-factory-import")
    def collection_factory_import():
        return "collection_factory_import"

    @app.route("/current-app-import")
    def current_app_import():
        return "current_app_import"
