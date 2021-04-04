from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    sent_messages_id = db.Column(db.Integer, db.ForeignKey("message.message_id"))
    received_messages_id = db.Column(db.Integer, db.ForeignKey("message.message_id"))

    sent_messages = relationship('Message', foreign_keys=[sent_messages_id], cascade="all", uselist=True)
    received_messages = relationship('Message', foreign_keys=[received_messages_id], cascade="all", uselist=True)

    # for validate authentication
    public_id = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f"User(user_name = {self.user_name}, email = {self.email})"


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), unique=False, nullable=False)
    subject = db.Column(db.String(100), unique=False, nullable=False)
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    read = db.Column(db.Boolean, default=False, unique=False, nullable=False)

    sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __repr__(self):
        return f"Message(message = {self.message} subject = {self.subject}, creation_date = {self.creation_date}"
