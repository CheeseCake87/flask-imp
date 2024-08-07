from flask import Flask


def collection(app: Flask):
    @app.context_processor
    def example__utility_processor():
        """
        Usage:
        {{ format_price(100.33) }} -> $100.33
        """

        def example__format_price(amount, currency="$"):
            return "{1}{0:.2f}".format(amount, currency)

        return dict(format_price=example__format_price)
