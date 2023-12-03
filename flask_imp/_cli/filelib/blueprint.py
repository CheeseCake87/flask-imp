from dataclasses import dataclass


@dataclass(frozen=True)
class BlueprintFileLib:
    # Format to: NONE
    init_py = """\
from flask_imp import Blueprint

bp = Blueprint(__name__)

bp.import_resources("routes")


@bp.before_app_request
def before_app_request():
    bp.init_session()
"""

    # Format to: name, url_prefix
    config_toml = """\
ENABLED = "yes"

[SETTINGS]
URL_PREFIX = "/{url_prefix}"
#SUBDOMAIN = ""
#URL_DEFAULTS = {{}}
STATIC_FOLDER = "static"
TEMPLATE_FOLDER = "templates"
STATIC_URL_PATH = "/static"
#ROOT_PATH = ""
#CLI_GROUP = ""

[SESSION]
#{name}_session = "yes"

# Set ENABLED to true to allow the blueprint
# to create a database bind, change settings accordingly.
[DATABASE_BIND]
ENABLED = false
DIALECT = "sqlite"
DATABASE_NAME = "{name}"
LOCATION = ""
PORT = ""
USERNAME = ""
PASSWORD = ""
"""

    # Format to: Name
    routes_index_py = """\
from flask import render_template

from pyhead import Head

from .. import bp


@bp.route("/", methods=["GET"])
def index():
    head = Head(title="Flask Imp Blueprint: {name}")
    return render_template(
        bp.tmpl("index.html"),
        head=head
    )
"""

    # Format to: root, name, flask_imp_logo
    templates_index_html = """\
{{% extends '{name}/extends/main.html' %}}

{{% block content %}}
    <div style="display: flex; flex-direction: row; align-items: center; gap: 2rem; margin-bottom: 2rem;">
        <div>
            <h2 style="margin: 0;">Blueprint: {name}</h2>
            <h3>Here's your new blueprint.</h3>
            <p>Located here: <code>{root}</code></p>
            <p style="margin-bottom: 0;">Remember to double-check the config.toml file.</p>
        </div>
    </div>
{{% endblock %}}
"""

    # Format to: name, flask_imp_logo, index_html, extends_main_html, index_py, init_py
    ia_templates_index_html = """\
{{% extends 'www/extends/main.html' %}}

{{% block content %}}
<div style="display: flex; flex-direction: row; align-items: center; gap: 2rem; margin-bottom: 2rem;">
    <div>
        <h2 style="margin: 0;">Blueprint: {name}</h2>
        <h3>This is the index route of the included example blueprint.</h3>
        <p style="margin-bottom: 0;">
            This template page is located in <code>{index_html}</code><br/>
            it extends from <code>{extends_main_html}</code><br/>
            with its route defined in <code>{index_py}</code><br/><br/>
            It's being imported by <code>bp.import_resources("routes")</code>
            in the <code>{init_py}</code> file.
        </p>
    </div>
</div>
{{% endblock %}}
"""

    # Format to: head_tag
    templates_extends_main_html = """\
<!doctype html>

<html lang="en">
<head>
    {head_tag}
</head>

<body>
{{% include '{name}/includes/header.html' %}}
{{% block content %}}{{% endblock %}}
{{% include '{name}/includes/footer.html' %}}
</body>

</html>
"""

    # Format to: header_html, main_html
    templates_includes_header_html = """\
<div style="display: flex; flex-direction: row; align-items: center;
            justify-content: start; gap: 2rem; margin-bottom: 2rem;">
    <img style="border-radius: 50%"
         src="{{{{ url_for('{static_path}', filename='img/flask-imp-logo.png') }}}}" alt="flask-imp logo">
    <h1 style="font-size: 4rem;">Flask-Imp</h1>
</div>
<div style="margin-bottom: 2rem;">
    <p>This is the header, located here: <code>{header_html}</code></p>
    <p>It's being imported in the <code>{main_html}</code> template.</p>
</div>
"""

    # Format to: footer_html, main_html
    templates_includes_footer_html = """\
<div style="display: flex; flex-direction: row; align-items: center; gap: 2rem; margin-bottom: 2rem;">
    <div>
        <p>This is the footer, located here: <code>{footer_html}</code></p>
        <p>It's being imported in the <code>{main_html}</code> template.</p>
    </div>
</div>
"""
