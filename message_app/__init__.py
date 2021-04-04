from flask import Flask
from message_app.config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from .db.database import connect_to_db
from .db.create_tables import create_all


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    connect_to_db(app)

    with app.app_context():
        import message_app.api.routes
        import message_app.auth.routes
        create_all(app)

    return app


app = create_app()
