from flask import current_app
from flask import g
from markupsafe import Markup
from flask import render_template
from ..functions.auth import generate_password
from ..functions.email_connector import test_email_server_connection


@current_app.route('/core/func-test', endpoint="core.func_test")
def func_test():
    return generate_password(style="animals", length=3)


@current_app.route('/core/test-email-settings', endpoint="core.test_email_settings")
def test_email():
    email_test_return = test_email_server_connection()
    return f"""{email_test_return[0]}, {email_test_return[1]}, {email_test_return[2]}"""


@current_app.route('/core/elements', endpoint="core.elements")
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


@current_app.route('/core/endpoints', endpoint="core.endpoints")
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


@current_app.route('/core/database', endpoint="core.database")
def database():
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
