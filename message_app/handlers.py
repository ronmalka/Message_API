from flask import current_app as app
from message_app.db.models import User, Message
from message_app.db.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import uuid


def get_all_messages_handler(user_id, unread):
    receiver = User.query.filter_by(user_id=user_id).first()

    if receiver is None:
        return None, "This User Does Not Exist"

    messages = Message.query.filter_by(receiver_id=user_id)
    if unread == 1:
        messages = messages.filter_by(read=False)

    return messages.all(), "OK"


# a user that does not exist not allowed to send or to receive a message

def write_message_handler(user_id, receiver_id, message, subject):
    sender_id = user_id
    sender = User.query.filter_by(user_id=sender_id).first()

    if sender is None:
        return None, "sender_not_found"

    receiver = User.query.filter_by(user_id=receiver_id).first()

    if receiver is None:
        return None, "reciever_not_found"

    new_message = Message(message=message, subject=subject, sender_id=sender_id, receiver_id=receiver_id)

    sender.sent_messages.append(new_message)

    receiver.received_messages.append(new_message)

    # save changes
    db.session.add(new_message)
    db.session.commit()

    return new_message, "OK"


def read_message_handler(user_id, message_id):
    receiver = User.query.filter_by(user_id=user_id)

    if receiver is None:
        return None

    message = Message.query.filter_by(message_id=message_id).first()

    if message is None:
        return None

    message.read = True

    db.session.add(message)
    db.session.commit()

    return message


def delete_message_handler(user_id, message_id):
    message = Message.query.filter_by(message_id=message_id).first()

    if message is None:
        return "Message Does Not Exist"

    if user_id != message.sender_id and user_id != message.receiver_id:
        return "An invalid user trying to delete this message"

    db.session.delete(message)
    db.session.commit()

    return "OK"


def get_user_handler(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if user is None:
        return None

    return user


def login_handler(auth):
    email = auth['email']
    password = auth['password']
    if not auth or not email or not password:
        # returns 401 if any email or / and password is missing
        return None, 'Basic realm ="Login required !!"', 401

    user = User.query.filter_by(email=email).first()

    if not user:
        # returns 401 if user does not exist
        return None, 'Basic realm ="User does not exist !!"', 401

    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        payload = {
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(days=30)
        }
        token = jwt.encode(
            payload,
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        return token, "OK", 201
    # returns 403 if password is wrong
    return None, 'Basic realm ="Wrong Password !!"', 403


def signup_handler(user_name, email, password):
    # checking for existing user
    user = User.query \
        .filter_by(email=email) \
        .first()
    if not user:
        # database ORM object
        user = User(
            public_id=str(uuid.uuid4()),
            user_name=user_name,
            email=email,
            password=generate_password_hash(password)
        )
        # insert user
        db.session.add(user)
        db.session.commit()

        return 'Successfully registered.', 201
    else:
        # returns 202 if user already exists
        return 'User already exists. Please Log in.', 202
