import unittest
from flaskr import create_app, db
from tests import db_drop_everything


class CorsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db_drop_everything(db)
        self.app_context.pop()

    def test_cors(self):
        response = self.client.head('/')

        self.assertIn('Access-Control-Allow-Origin', response.headers)
        self.assertEqual('*', response.headers['Access-Control-Allow-Origin'])
        self.assertIn('Access-Control-Allow-Headers', response.headers)
        self.assertEqual('Content-Type', response.headers['Access-Control-Allow-Headers'])
        self.assertIn('Access-Control-Allow-Methods', response.headers)
        self.assertEqual('GET, PATCH, POST, DELETE, OPTIONS', response.headers['Access-Control-Allow-Methods'])
