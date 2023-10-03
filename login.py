import hashlib
from datetime import datetime, timedelta

import jwt
from flask import request, make_response, jsonify, Blueprint
from werkzeug.exceptions import Unauthorized

from tables import User

login_blueprint = Blueprint('login', __name__, url_prefix='/login')


def decode_token(token):
    try:
        return jwt.decode(token, 'very_important_secret', algorithms=['HS256'])
    except Exception as e:
        raise Unauthorized from e


@login_blueprint.route('', methods=['POST'])
def login():
    password = request.json.get('password', None)

    if not password:
        return make_response('Password is missing', 401)
    hash_password = hashlib.sha256(password.encode('UTF-8')).hexdigest()
    user = User.query.get('1')  # hardcoded user_id since we have only one user
    if not hash_password == user.password:
        return make_response('Contains invalid credentials', 401)

    token = jwt.encode({'public_id': '1', 'exp': datetime.utcnow() + timedelta(minutes=30)}, 'very_important_secret')
    return make_response(jsonify({'token': token}))
