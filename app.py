




app = create_app('config.DevelopmentConfig', config_pyfile='development.py')
migrate = Migrate(app, db)
manager = Manager(app)