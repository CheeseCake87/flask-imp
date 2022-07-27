from flask import jsonify
from ..functions.api_auth import public_key_required

from .. import api_bp


@api_bp.route('/test')
class Test():
    def get(self):
        return jsonify(Response="GET Method")

    def post(self, public_key):
        public_key_required(public_key)
        return jsonify(Response="POST Method")
