from flask_migrate import Migrate
from flask_restful import Api

from app import create_app
from app.database import db
from app.routes import configure_routes


# TODO: load settings from envvars

app = create_app(config_pyfile='config.py')
migrate = Migrate(app, db)
api = Api(app)
configure_routes(api)
