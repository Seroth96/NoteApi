import os
from datetime import timedelta
SECRET_KEY = 'super-secret'

#Define absolute path to the directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False


JWT_AUTH_URL_RULE = "/api/login"
JWT_AUTH_ENDPOINT = "login"
JWT_EXPIRATION_DELTA = timedelta(seconds=100000)
