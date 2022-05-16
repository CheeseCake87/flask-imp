from ..functions.api_auth import public_key_required
from flask_restx import Resource

from .. import api


@api.route('/test')
class Test(Resource):
    def get(self):
        return "waiting"

    def post(self, public_key):
        public_key_required(public_key)
        return """API POST"""

