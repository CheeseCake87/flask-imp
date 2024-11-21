from flask import current_app as app


@app.context_processor
def example__utility_processor():
    """
    Usage:
    {{ example__format_price(100.33) }} -> $100.33
    """

    def example__format_price(amount, currency="$"):
        return "{1}{0:.2f}".format(amount, currency)

    return dict(example__format_price=example__format_price)
