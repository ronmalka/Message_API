from flask import request, jsonify, current_app as app
from functools import wraps
from message_app.db.models import User
import jwt


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header

        token = request.headers['AUTHORIZATION']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        current_user = User.query.filter_by(public_id=payload['public_id']).first()

        try:
            message_id = kwargs['message_id']
        except:
            return f(current_user.user_id)

        return f(current_user.user_id, message_id)

    return decorated
