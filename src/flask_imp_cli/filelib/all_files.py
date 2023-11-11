class GlobalFileLib:
    # Format to: app_name
    collections_cli_py = """\
from flask import current_app as app
from {app_name}.extensions import db
from {app_name}.models.example_user_table import ExampleUserTable


@app.cli.command("create-tables")
def create_tables():
    db.create_all()


@app.cli.command("get-example-user")
def get_example_user():
    result = ExampleUserTable.get_by_id(1)
    if not result:
        print("User not found.")
        return
    print(
        f\"\"\"
        user_id: {{result.user_id}}
        username: {{result.username}}
        salt: {{result.salt}}
        password: {{result.password}}
        private_key: {{result.private_key}}
        disabled: {{result.disabled}}
        \"\"\"
    )


@app.cli.command("create-example-user")
def add_example_user():
    ExampleUserTable.create(
        username="admin",
        password="password",
        disabled=False,
    )


@app.cli.command("update-example-user")
def update_example_user():
    ExampleUserTable.update(
        user_id=1,
        username="admin-updated",
        private_key="private_key",
        disabled=False,
    )


@app.cli.command("delete-example-user")
def delete_example_user():
    ExampleUserTable.delete(
        user_id=1,
    )
"""

    # Format to: None
    collections_context_processors_py = """\
from flask import current_app as app


@app.context_processor
def example__utility_processor():
    \"""
    Usage:
    {{ format_price(100.33) }} -> $100.33
    \"""

    def example__format_price(amount, currency='$'):
        return '{1}{0:.2f}'.format(amount, currency)

    return dict(format_price=example__format_price)
"""

    # Format to: None
    collections_error_handlers_py = """\
from flask import current_app as app
from flask import render_template


@app.errorhandler(400)
def error_400(error):
    return render_template(
        "errors/400.html",
    ), 400


@app.errorhandler(401)
def error_401(error):
    return render_template(
        "errors/401.html",
    ), 401


@app.errorhandler(403)
def error_403(error):
    return render_template(
        "errors/403.html",
    ), 403


@app.errorhandler(404)
def error_404(error):
    return render_template(
        "errors/404.html",
    ), 404


@app.errorhandler(405)
def error_405(error):
    return render_template(
        "errors/405.html",
    ), 405


@app.errorhandler(500)
def error_500(error):
    return render_template(
        "errors/500.html",
    ), 500
"""

    # Format to: None
    collections_filters_py = """\
from flask import current_app as app


@app.template_filter('example__num_to_month')
def example__num_to_month(num: str) -> str:
    \"""
    Usage:
    {{ 1 | example__num_to_month }} -> January
    \"""
    if isinstance(num, int):
        num = str(num)

    months = {
        "1": "January",
        "2": "February",
        "3": "March",
        "4": "April",
        "5": "May",
        "6": "June",
        "7": "July",
        "8": "August",
        "9": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }

    if num in months:
        return months[num]
    return "Month not found"
"""

    # Format to: None
    collections_routes_py = """\
from flask import current_app as app
from flask import render_template


@app.route("/global")
def index():
    return render_template(
        "index.html",
    )
"""

    # Format to: name
    static_main_js = """\
console.log('This log is from the file global/static/js/main.js')
"""

    # Format to: None
    templates_extends_main_html = """\
<!doctype html>

<html lang="en">
<head>

{#    https://github.com/joshbuchea/HEAD #}

    <title>{% block title %}{% endblock %}Flask-Imp</title>
    <base href="{{ request.base_url }}">

    <!-- Security -->
{#    <meta http-equiv="Content-Security-Policy" content="script-src 'self' 'unsafe-inline' 'unsafe-eval';">#}

    <!-- Bots -->
    <meta name="robots" content="index,follow">
    <meta name="googlebot" content="index,follow">

    <!-- General Settings -->
    <meta charset="utf-8">
    <meta http-equiv="x-dns-prefetch-control" content="off">
    <meta name="google" content="nositelinkssearchbox">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="msapplication-TileColor" content="#da532c">
    <meta name="theme-color" content="#ffffff">
    <meta name=”rating” content=”general”>
    <meta name="referrer" content="no-referrer">
    <meta name="format-detection" content="telephone=no">

    <!-- GEO location -->
    <meta name="ICBM" content="55.86012186235461, -4.252010320043988">
    <meta name="geo.position" content="55.86012186235461;-4.252010320043988">
    <meta name="geo.region" content="GB-SCT">
    <meta name="geo.placename" content="Glasgow">
    <meta name="DC.title" content="Flask-Imp"/>

    <!-- Page Specific -->
    <meta name="rating" content="general">
    <meta name="subject" content="your document's subject">
    <meta name="description" content="A description of the page">

    <!-- site verification -->
{#    <meta name="google-site-verification" content="verification_token"><!-- Google Search Console -->#}
{#    <meta name="yandex-verification" content="verification_token"><!-- Yandex Webmasters -->#}
{#    <meta name="msvalidate.01" content="verification_token"><!-- Bing Webmaster Center -->#}
{#    <meta name="alexaVerifyID" content="verification_token"><!-- Alexa Console -->#}
{#    <meta name="p:domain_verify" content="code_from_pinterest"><!-- Pinterest Console-->#}
{#    <meta name="norton-safeweb-site-verification" content="norton_code"><!-- Norton Safe Web -->#}

    <!-- facebook -->
{#    <meta property="fb:app_id" content="123456789">#}
    <meta property="og:url" content="{{ request.base_url }}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Flask-Imp">
{#    <meta property="og:image" content="~ static folder here ~/facebook-image.png">#}
    <meta property="og:image:alt" content="A description of what is in the image (not a caption)">
    <meta property="og:description" content="Description Here">
    <meta property="og:site_name" content="Flask-Imp Website">
    <meta property="og:locale" content="en_GB">
    <meta property="article:author" content="">

    <!-- twitter -->
    <meta name="twitter:card" content="summary">
    <meta name="twitter:site" content="@site_account">
{#    <meta name="twitter:creator" content="@individual_account">#}
    <meta name="twitter:url" content="{{ request.base_url }}">
    <meta name="twitter:title" content="Flask-Imp Website">
    <meta name="twitter:description" content="Content description less than 200 characters">
{#    <meta name="twitter:image" content="~ static folder here ~/twitter-image.png">#}
    <meta name="twitter:image:alt" content="Description of the image (for visually impaired). Maximum 420 characters.">

    <!-- pinterest - disabled -->
    <meta name="pinterest" content="nopin">

    <!-- pre-loadings -->
{#    https://css-tricks.com/prefetching-preloading-prebrowsing/ #}
{#    <link rel="dns-prefetch" href="//example.com/">#}
{#    <link rel="preconnect" href="https://www.example.com/">#}
{#    <link rel="prefetch" href="example.font.ttf">#}
{#    <link rel="prerender" href="https://example.com/">#}
{#    <link rel="preload" href="image.png" as="image">#}

    <!-- favicons -->
{#    <link rel="apple-touch-icon" sizes="152x152" href="~ static folder here ~/152x152-favicon.png">#}
{#    <link rel="icon" type="image/png" sizes="32x32" href="~ static folder here ~/32x32-favicon.png">#}
{#    <link rel="icon" type="image/png" sizes="16x16" href="~ static folder here ~/16x16-favicon.png">#}
{#    <link rel="manifest" href="~ static folder here ~/site.webmanifest">#}

    <link rel="stylesheet" href="{{ url_for('static', filename='css/water.css') }}">

    <script defer src="{{ url_for('static', filename='js/main.js') }}"></script>

    <script>
        // inline script
    </script>

</head>

<body>
{% include "includes/header.html" %}
{% block content %}{% endblock %}
{% include "includes/footer.html" %}
</body>
</html>
"""

    # Format to: None
    templates_includes_footer_html = """\
<hr/>
<p>This is the footer, this is located here: <code>global/templates/includes/footer.html</code></p>
<p>It's being imported in the <code>global/templates/extends/main.html</code> template.</p>
"""

    # Format to: flask_imp_logo
    templates_includes_header_html = """\
<div style="display: flex; flex-direction: row; align-items: center; gap: 2rem; margin-bottom: 2rem;">
    <img style="border-radius: 50%"
         src="{flask_imp_logo}" alt="logo">
    <div>
        <h1 style="margin: 0;">Flask-Imp</h1>
        <p>This is the header, this is located here: <code>global/templates/includes/header.html</code></p>
        <p>It's being imported in the <code>global/templates/extends/main.html</code> template.</p>
    </div>
</div>
"""

    # Format to: None
    templates_index_html = """\
{% extends 'extends/main.html' %}


{% block content %}

    <p>This is the template file located in <code>global/templates/index.html</code></p>

{% endblock %}
"""

    templates_errors_400_html = """\
<!doctype html>
<html lang="en">

<head>
    <title>400 Bad Request</title>
</head>

<body>
<p>It's not us, it's you.</p>
</body>
</html>
"""

    templates_errors_401_html = """\
<!doctype html>
<html lang="en">

<head>
    <title>401 Unauthorized</title>
</head>

<body>
<p>You lack valid authentication credentials for the requested resource</p>
</body>
</html>
"""

    templates_errors_403_html = """\
<!doctype html>
<html lang="en">

<head>
    <title>403 Forbidden</title>
</head>

<body>
<p>Access forbidden!</p>
</body>
</html>
"""

    templates_errors_404_html = """\
<!doctype html>
<html lang="en">

<head>
    <title>404 Page Not Found</title>
</head>

<body>
<p>No route associated with the URL</p>
</body>
</html>
"""

    templates_errors_405_html = """\
<!doctype html>
<html lang="en">

<head>
    <title>405 Method Not Allowed</title>
</head>

<body>
<p>Should of GET when you POST, or POST when you GET</p>
</body>
</html>
"""

    templates_errors_500_html = """\
<!doctype html>
<html lang="en">

<head>
    <title>500 Server Error!</title>
</head>

<body>
<p>There has been a server error!</p>
</body>
</html>
"""
