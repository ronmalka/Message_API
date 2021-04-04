import os

DB_NAME = "database.db"
DATABASE_PATH = os.path.realpath(os.getcwd()) + DB_NAME
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
SECRET_KEY = "this is very very secret"
