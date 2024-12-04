def head_tag_generator(static_url_endpoint: str = "static", no_js: bool = False) -> str:
    """Generate the head tag for the HTML template files."""

    js = (
        (
            f"<script defer src=\"{{{{ url_for('{static_url_endpoint}', "
            f"filename='js/main.js') }}}}\"></script>"
        )
        if not no_js
        else ""
    )

    favicon = (
        '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http'
        "://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text "
        'y=%22.9em%22 font-size=%2290%22>🧚</text></svg>">'
    )

    return f"""\
<meta charset="utf-8">
    <meta name="viewport" content="'width=device-width, initial-scale=1'">
    <title>Flask-Imp</title>
    {favicon}
    <link rel="stylesheet" href="{{{{ url_for('{static_url_endpoint}', filename='css/water.css') }}}}">
    {js}

    <script>
        // inline script
    </script>
"""
