from flask import current_app


@current_app.before_first_request
def before_first_request():
    pass


@current_app.before_request
def before_request():
    pass


@current_app.after_request
def after_request(response):
    return response
