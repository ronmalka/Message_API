import json

from flask import request, jsonify, make_response
from flask_restful import abort
from flask import current_app as app

from message_app.auth.helpers import token_required
from message_app.handlers import get_user_handler, login_handler, signup_handler


# AUTH ROUTES

# route for login user in
@app.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = json.loads(request.data)

    token, error, code = login_handler(auth)

    if error != "OK":
        return make_response(
            'Could not verify',
            code,
            {'WWW-Authenticate': error}
        )

    return make_response(jsonify({'token': token}), code)


# signup route
@app.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = json.loads(request.data)

    user_name = data['user_name']
    email = data['email']
    password = data['password']

    message, code = signup_handler(user_name, email, password)

    return make_response(message, code)


# USER ROUTES

@app.route('/users/<int:user_id>', methods=["GET"])
@token_required
def get_user(user_id):
    # data = json.loads(request.data)
    user = get_user_handler(user_id)

    if user is None:
        abort(404, message="This User Does Not Exist")

    return jsonify({
        "user_id": user.user_id,
        "user_name": user.user_name,
        "user_email": user.email,
        "status": 200
    })
