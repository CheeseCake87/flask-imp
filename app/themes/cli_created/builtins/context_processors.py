def loader(app):
    @app.context_processor
    def utility_processor():
        """
        Usage

        {{ format_price(100) }}
        {{ format_price(100.33) }}
        """

        def format_price(amount, currency='$'):
            return '{1}{0:.2f}'.format(amount, currency)

        return dict(format_price=format_price)
