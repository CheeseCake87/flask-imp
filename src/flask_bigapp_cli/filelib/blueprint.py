class BlueprintFileLib:
    # Format to: NONE
    init_py = """\
from flask_bigapp import Blueprint

bp = Blueprint(__name__)

bp.import_resources("routes")


@bp.before_app_request
def before_app_request():
    bp.init_session()
"""

    # Format to: name, url_prefix
    config_toml = """\
enabled = "yes"

[settings]
url_prefix = "/{url_prefix}"
#subdomain = ""
#url_defaults = {{}}
static_folder = "static"
template_folder = "templates"
static_url_path = "/static/{name}"
#root_path = ""
#cli_group = ""

[session]
#{name}_session = "yes"
"""

    # Format to: NONE
    routes_index_py = """\
from flask import render_template

from .. import bp


@bp.route("/", methods=["GET"])
def index():
    return render_template(bp.tmpl("index.html"))
"""

    # Format to: name, location
    templates_index_html = """\
{{% extends '{name}/extends/main.html' %}}

{{% block content %}}
    <div style="display: flex; flex-direction: row; align-items: center; gap: 2rem; margin-bottom: 2rem;">
        <img style="border-radius: 50%"
             src="{{{{ url_for('{name}.static', filename='Flask-BigApp-Logo.svg') }}}}" alt="logo">
        <div>
            <h1 style="margin: 0;">{name} blueprint</h1>
            <cite>
                <h3>Here's your new blueprint.</h3>
                <p>Remember to double-check the config.toml file.
                <p/>
            </cite>
        </div>
    </div>
{{% endblock %}}
"""

    # Format to: name
    templates_extends_main_html = """\
<!doctype html>

<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Blueprint: {name}</title>
    <link rel="stylesheet" href="{{{{ url_for('{name}.static', filename='water.css') }}}}">
</head>

<body>
{{% block content %}}

{{% endblock %}}
</body>

</html>
"""


class InitAppBlueprintFileLib:
    # Format to: name, url_prefix
    config_toml = """\
enabled = "yes"

[settings]
url_prefix = "/{url_prefix}"
#subdomain = ""
#url_defaults = {{}}
#static_folder = "static"
template_folder = "templates"
#static_url_path = "/static/{name}"

[session]
#{name}_session = "yes"
"""

    templates_index_html = """\
{{% extends 'extends/main.html' %}}

{{% block content %}}
    <div style="margin-bottom: 2rem;">
        <cite>
            This is the index route of the included example blueprint.<br/>
            This template page is located in <code>blueprints/www/templates/www/index.html</code><br/>
            it extends from <code>global/templates/extends/main.html</code><br/>
            with it's route defined in <code>blueprints/www/routes/index.py</code><br/><br/>
            It's being auto imported by <code>bp.import_resources("routes")</code> <br/>
            in the <code>blueprints/www/__init__.py</code> file.
        </cite>
    </div>
{{% endblock %}}
"""
