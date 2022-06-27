from flask import current_app

from .. import bp


@bp.route("/app-models", methods=["GET"])
def app_models():
    """
    Lists the model information loaded into app.config['models'] by FlaskLaunchpad
    """
    output = ""
    for key, value in current_app.config["models"].items():
        output += f"{key} : {value} <br/>"
    return output


@bp.route("/app-url-map", methods=["GET"])
def app_url_map():
    """
    Outputs all Flasks URLs
    """
    output = ""
    for rule in current_app.url_map.iter_rules():
        output += f"{rule.endpoint} : {rule.rule} <br/>"
    return output
