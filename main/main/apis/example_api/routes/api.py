import json
from json import loads
from flask import request
from flask import abort
from flask_restx import Resource
from ....builtins.functions.email import test_email_server_connection
from ....builtins.functions.email import send_email
from ....builtins.functions.auth import generate_password
from ..functions.api_auth import check_http_auth
from ..functions.api_auth import public_key_correct
from .. import api
from ..crud import if_account_not_found
from ..crud import if_account_is_found
from ..crud import authenticate_request_failed
from ..crud import sign_in
from ..crud import sign_up
from ..crud import update_password


@api.route('/login/<string:public_key>')
class Login(Resource):
    def get(self, public_key):
        if not public_key_correct(public_key):
            return abort(404)
        return "waiting"

    def post(self, public_key):
        if not public_key_correct(public_key):
            abort(404)

        payload = loads(request.data.decode('utf-8'))
        _sign_in = sign_in(username=payload["username"], password=payload["password"])

        if _sign_in["return"]:
            return {
                "status": "200",
                "account_id": _sign_in["account_id"],
                "private_key": _sign_in["private_key"],
            }

        return abort(401)


@api.route('/signup/<string:public_key>')
class Signup(Resource):
    def get(self, public_key):
        if not public_key_correct(public_key):
            return abort(404)
        return "waiting"

    def post(self, public_key):
        if not public_key_correct(public_key):
            return abort(404)

        payload = loads(request.data.decode('utf-8'))

        # check if account is already there
        if if_account_is_found(payload["email_address"]):
            return abort(406)

        _sign_up = sign_up(
            username=payload["username"],
            password=payload["password"]
        )

        if _sign_up["return"]:
            return {
                "status": "200",
                "message": "Account created"
            }
        return abort(401)


@api.route('/forgotpassword/<string:public_key>')
class ForgotPassword(Resource):
    def get(self, public_key):
        if not public_key_correct(public_key):
            return abort(404)
        return "waiting"

    def post(self, public_key):
        if not public_key_correct(public_key):
            return abort(404)

        payload = loads(request.data.decode('utf-8'))

        if if_account_not_found(payload["email_address"]):
            return abort(406)

        if test_email_server_connection()[0]:
            new_password = generate_password("animals", 3)
            update_password(payload["email_address"], new_password)
            send_email(
                "Password reset",
                payload["email_address"],
                f"""
                Your new password is:
                {new_password}
                """
            )
            return {
                "status": "200",
                "message": "Password emailed"
            }

        return abort(401)

