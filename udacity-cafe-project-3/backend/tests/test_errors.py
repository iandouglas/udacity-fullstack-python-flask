import json
import unittest
from api import create_app, db
from tests import db_drop_everything, seed_data, assert_value_type


class ErrorsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        seed_data(db)
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db_drop_everything(db)
        self.app_context.pop()

    def test_404_error(self):
        response = self.client.get('/lkjasdkj')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))

        assert_value_type(self, data, 'error', str, 'resource not found')
        assert_value_type(self, data, 'error', int, 404)
        assert_value_type(self, data, 'success', bool, False)
