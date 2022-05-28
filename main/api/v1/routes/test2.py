from ..functions.api_auth import public_key_required
from flask_restx import Resource

from .. import api


@api.route('/test2')
class Test2(Resource):
    def get(self):
        return "GET Method"

    def post(self, public_key):
        public_key_required(public_key)
        return """POST Method"""

