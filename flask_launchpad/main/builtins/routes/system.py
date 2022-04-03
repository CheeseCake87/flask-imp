from flask import current_app
from flask import request
from markupsafe import Markup
from flask import render_template
from ..functions.auth import generate_password


@current_app.route('/system/test', endpoint="system.test")
def element_test():
    return generate_password(style="animals", length=3)


@current_app.route('/system/elements', endpoint="system.elements")
def element_test():
    render_args = {}

    def args() -> dict:
        render_args['template_name_or_list'] = "renders/elements.html"
        render_args['structure'] = "structures/default.html"
        render_args['title'] = "Element Overview"
        render_args['keywords'] = "element, overview"
        render_args['description'] = "Contains examples of all the Elements that can be made"
        return {**render_args}

    return render_template(**args())


@current_app.route('/system/endpoints', endpoint="system.endpoints")
def display_endpoints():
    endpoints = {}
    endpoint_text = ""
    for rule in current_app.url_map.iter_rules():
        endpoints[rule.endpoint] = rule.rule

    for endpoint, url in sorted(endpoints.items()):
        endpoint_text += f"""
        <tr>
        <td style="text-align:right;">{endpoint}</td>
        <td> : </td>
        <td>{url}</td>
        </tr>
        """

    table = f"""
    <h1>Available Endpoints</h1>
    <table>
    {endpoint_text}
    </table>
    """
    return Markup(table)


@current_app.route("/system/locked-page", endpoint="system.locked_page")
def locked_page():
    return """This page is locked."""


@current_app.route("/system/redirect-success", endpoint="system.redirect_success")
def redirect_success():
    return """A function has returned successful if you have been redirected here."""


@current_app.route("/system/redirect-catch-all", endpoint="system.redirect_catch_all")
def redirect_catch_all():
    re_var = """
    This is a redirect catch all.
    """
    endpoints = {}
    endpoint_text = ""
    for rule in current_app.url_map.iter_rules():
        endpoints[rule.endpoint] = rule.rule

    for endpoint, url in sorted(endpoints.items()):
        endpoint_text += f"""
        <tr>
        <td style="text-align:right;">{endpoint}</td>
        <td> : </td>
        <td>{url}</td>
        </tr>
        """

    if "tried" in request.args:
        re_var = f"""
        The endpoint: {request.args['tried']} does not exist
        <br/>
        <br/>
        Here are the available endpoints:
        <br/>
        <br/>
        <table>
        {endpoint_text}
        </table>
        """
    return Markup(re_var)
