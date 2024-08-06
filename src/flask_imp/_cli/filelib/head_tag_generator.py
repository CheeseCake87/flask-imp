def head_tag_generator(static_endpoint="static", no_js=False):
    """Generate the head tag for the HTML template files."""

    js = (
        (
            f"<script defer src=\"{{{{ url_for('{static_endpoint}', "
            f"filename='js/main.js') }}}}\"></script>"
        )
        if not no_js
        else ""
    )

    favicon = (
        '<link rel="icon" href="{{ url_for(\'static\', '
        'filename=\'favicon.ico\') }}" sizes="16x16 32x32" '
        'type="image/x-icon">'
    )

    return f"""\
<meta charset="utf-8">
    <meta name="viewport" content="'width=device-width, initial-scale=1.0'">
    <title>Flask-Imp</title>
    {favicon}
    <link rel="stylesheet" href="{{{{ url_for('{static_endpoint}', filename='css/water.css') }}}}">
    {js}

    <script>
        // inline script
    </script>
"""
