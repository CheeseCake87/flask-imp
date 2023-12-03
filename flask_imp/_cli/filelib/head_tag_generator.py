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

    return f"""\
    {{{{ head() }}}}

    <link rel="stylesheet" href="{{{{ url_for('{static_endpoint}', filename='css/water.css') }}}}">
    {js}

    <script>
        // inline script
    </script>
"""
