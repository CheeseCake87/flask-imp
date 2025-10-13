def templates_minimal_index_html(
    head_tag: str, index_py: str, index_html: str, init_py: str
) -> str:
    return f"""\
<!doctype html>

<html lang="en">
<head>
{head_tag}
</head>

<body>
<div style="display: flex; flex-direction: row; align-items: center;
            justify-content: start; gap: 2rem; margin-bottom: 2rem;">
    <h1 style="font-size: 4rem;">Flask-Imp 🧚</h1>
</div>
<div style="display: flex; flex-direction: row; align-items: center; gap: 2rem; margin-bottom: 2rem;">
    <div>
        <p style="margin-bottom: 0;">
            This template page is located in <code>{index_html}</code><br/>
            with its route defined in <code>{index_py}</code><br/><br/>
            It's being imported by <code>app.import_resources()</code>
            in the <code>{init_py}</code> file.
        </p>
    </div>
</div>
</body>

</html>
"""


def templates_error_html() -> str:
    return """\
<!doctype html>
<html lang="en">

<head>
    <title>{{ error_code }}</title>
</head>

<body>
<h1>{{ error_code }}</h1>
<p>{{ error_message }}</p>
</body>
</html>
"""
