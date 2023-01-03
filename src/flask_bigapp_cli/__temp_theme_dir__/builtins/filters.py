def loader(app):
    from markupsafe import Markup

    @app.template_filter('example')
    def filter_(value: str) -> str:
        """
        Usage

        {{ "hello" | example }} = The string value passed in is: hello -> here is something after that value.
        """
        return Markup(f"The string value passed in is: {value} -> here is something after that value.")
