import os

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@localhost/{}'.format(
    db_user, db_password, db_name,
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
