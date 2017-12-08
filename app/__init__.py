from flask import Flask


def create_app(config_object=None, config_pyfile=None):
    app = Flask(__name__)

    # app settings
    if config_object:
        app.config.from_object(config_object)
    if config_pyfile:
        app.config.from_pyfile(config_pyfile)

    # configure database
    from .database import db, init_db
    init_db(db, app)

    return app
