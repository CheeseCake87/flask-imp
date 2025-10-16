from pathlib import Path

from ..helpers import strip_leading_slash


def blueprint_init_py(url_prefix: str, name: str) -> str:
    return f"""\
from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig


bp = ImpBlueprint(__name__, ImpBlueprintConfig(
    enabled=True,
    url_prefix="/{strip_leading_slash(url_prefix)}",
    static_folder="static",
    template_folder="templates",
    init_session={{"{name}_session_loaded": True}},
))

bp.import_resources()
"""


def blueprint_resources_index_py() -> str:
    return """\
from flask import render_template
from flask_imp import ImpBlueprint


def include(bp: ImpBlueprint):
    @bp.route("/", methods=["GET"])
    def index():
        return render_template(bp.tmpl("index.html"))
"""


def blueprint_templates_index_html(blueprint_name: str, root: Path) -> str:
    return f"""\
{{% extends '{blueprint_name}/extends/main.html' %}}

{{% block content %}}
    <div style="display: flex; flex-direction: row; align-items: center; gap: 2rem; margin-bottom: 2rem;">
        <div>
            <h2 style="margin: 0;">Blueprint: {blueprint_name}</h2>
            <h3>Here's your new blueprint.</h3>
            <p>Located here: <code>{root}</code></p>
        </div>
    </div>
{{% endblock %}}
"""


def blueprint_init_app_templates_index_html(
    blueprint_name: str,
    index_html: Path,
    extends_main_html: Path,
    index_py: Path,
    init_py: Path,
) -> str:
    return f"""\
{{% extends 'www/extends/main.html' %}}

{{% block content %}}
<div style="display: flex; flex-direction: row; align-items: center; gap: 2rem; margin-bottom: 2rem;">
    <div>
        <h2 style="margin: 0;">Blueprint: {blueprint_name}</h2>
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


def blueprint_templates_extends_main_html(name: str, head_tag: str) -> str:
    return f"""\
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


def blueprint_templates_includes_header_html(header_html: Path, main_html: Path) -> str:
    return f"""\
<div style="display: flex; flex-direction: row; align-items: center;
            justify-content: start; gap: 2rem; margin-bottom: 2rem;">
    <h1 style="font-size: 4rem;">Flask-Imp 🧚</h1>
</div>
<div style="margin-bottom: 2rem;">
    <p>This is the header, located here: <code>{header_html}</code></p>
    <p>It's being imported in the <code>{main_html}</code> template.</p>
</div>
"""


def blueprint_templates_includes_footer_html(footer_html: Path, main_html: Path) -> str:
    return f"""\
<div style="display: flex; flex-direction: row; align-items: center; gap: 2rem; margin-bottom: 2rem;">
    <div>
        <p>This is the footer, located here: <code>{footer_html}</code></p>
        <p>It's being imported in the <code>{main_html}</code> template.</p>
    </div>
</div>
"""
