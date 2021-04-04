from message_app.config import DATABASE_PATH
from os import path
from .database import db
from .models import Message, User


def create_all(app):
    if not path.exists(DATABASE_PATH):
        db.create_all(app=app)
        print('Created Database!')
