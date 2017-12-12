import unittest

from app.database import db
from app.wsgi import app


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.db = db
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app_client = self.app.test_client()
        with self.app.app_context():
            self.db.session.close()
            self.db.drop_all()
            self.db.create_all()
