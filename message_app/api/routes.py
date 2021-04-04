from flask import request, current_app as app, jsonify

from message_app.auth.helpers import token_required
from message_app.handlers import *
from flask_restful import abort
import json


@app.route('/')
@app.route('/index')
def home():
    return 'Hello!'


def generate_message_json(message):
    return {
        "message_id": message.message_id,
        "sender_id": message.sender_id,
        "receiver_id": message.receiver_id,
        "message": message.message,
        "subject": message.subject,
        "read": message.read,
        "date": message.creation_date
    }


# MESSAGE ROUTES

@app.route('/users/<int:user_id>/messages', methods=['GET'])
@token_required
def get_all_messages(user_id):
    data = json.loads(request.data)
    unread = data['unread']
    messages, error = get_all_messages_handler(user_id, unread)

    if error != "OK":
        abort(404, message=error)

    user_messages = list(map(lambda message:
                             generate_message_json(message)
                             , messages))

    return jsonify({
        "messages": user_messages,
        "status": 200
    })


# user_id is the user sender id
@app.route('/users/<int:user_id>/message', methods=['POST'])
@token_required
def write_message(user_id):
    data = json.loads(request.data)

    receiver_id = data['receiver_id']
    message = data['message']
    subject = data['subject']

    message, error = write_message_handler(user_id, receiver_id, message, subject)
    if not message:
        if error == "reciever_not_found":
            abort(404, message="The Receiver User Does Not Exist")
        elif error == "sender_not_found":
            abort(404, message="The Sender User Does Not Exist")

    return jsonify({
        "message": generate_message_json(message),
        "status": 200
    })


@app.route('/users/<int:user_id>/messages/<int:message_id>', methods=['PATCH'])
@token_required
def read_message(user_id, message_id):
    message = read_message_handler(user_id, message_id)

    if not message:
        abort(404, message="This User or Message Does Not Exist")

    return jsonify({
        "message": generate_message_json(message),
        "status": 200
    })


@app.route('/users/<int:user_id>/messages/<int:message_id>', methods=['DELETE'])
@token_required
def delete_message(user_id, message_id):
    error = delete_message_handler(user_id, message_id)

    if error != "OK":
        abort(404, message=error)

    return jsonify({
        "status": 200
    })
