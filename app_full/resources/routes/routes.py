from flask import current_app as app


@app.route("/example--resources")
def example_route():
    return "From the [app_root]/resources/routes/routes.py file"
