from flask import Flask


def collection(app: Flask):
    @app.template_filter("example__num_to_month")
    def example__num_to_month(num: str) -> str:
        """
        Usage:
        {{ 1 | example__num_to_month }} -> January
        """
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
