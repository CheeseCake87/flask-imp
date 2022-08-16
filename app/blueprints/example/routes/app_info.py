from flask import current_app, render_template

from app import bigapp

from .. import bp


@bp.route("/app-models", methods=["GET"])
def app_models():
    """
    Lists the model information loaded into app.config['import_models'] by FlaskLaunchpad
    """
    models = bigapp.model_classes

    render = bp.render("app-models.html")
    extend = bigapp.extend("bigapp_default", "main.html")
    footer = bigapp.include("bigapp_default", "footer.html")

    return render_template(render, extend=extend, footer=footer, models=models)


@bp.route("/app-url-map", methods=["GET"])
def app_url_map():
    """
    Outputs all Flasks URLs
    """
    output = ""
    for rule in current_app.url_map.iter_rules():
        output += f"{rule.endpoint} : {rule.rule} <br/>"

    render = bp.render("app-url-map.html")
    extend = bigapp.extend("bigapp_default", "main.html")
    footer = bigapp.include("bigapp_default", "footer.html")

    return render_template(render, extend=extend, footer=footer, output=output)
