import json
import unittest
from unittest.mock import patch

from api import create_app, db
from api.database.models import Drink
from tests import db_drop_everything, seed_data, assert_payload_field_type_value, assert_payload_field_type

drink_id = None
BAD_DRINK_ID = 89745

class DeleteDrinksTest(unittest.TestCase):
    def setUp(self):
        global drink_id
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db_drop_everything(db)
        db.create_all()
        seed_data(db)
        drink = Drink(
            'blue water',
            [{
                "name": "Water",
                "color": "blue",
                "parts": 1
            }]
        )
        drink.insert()
        drink_id = drink.id

    def tearDown(self):
        db.session.remove()
        db_drop_everything(db)
        self.app_context.pop()


class GuestUserTest(DeleteDrinksTest):
    def test_endpoint_delete_drink(self):
        global drink_id
        if drink_id is not None:
            response = self.client.delete(f'/drinks/{drink_id}')

            self.assertEqual(401, response.status_code)
            data = json.loads(response.data.decode('utf-8'))
            assert_payload_field_type_value(self, data, 'error', int, 401)
            assert_payload_field_type_value(self, data, 'message', str, 'unauthorized')
            assert_payload_field_type_value(self, data, 'success', bool, False)

    def test_endpoint_delete_drink_bad_id(self):
        response = self.client.delete(f'/drinks/{BAD_DRINK_ID}')

        self.assertEqual(401, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'error', int, 401)
        assert_payload_field_type_value(self, data, 'message', str, 'unauthorized')
        assert_payload_field_type_value(self, data, 'success', bool, False)


class BaristaUserTest(DeleteDrinksTest):
    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_delete_drink(self, mock_get_token_auth_header, mock_verify_decode_jwt):
        global drink_id

        mock_get_token_auth_header.return_value = 'barista-token'
        mock_verify_decode_jwt.return_value = {'permissions': ['get:drinks-detail']}

        if drink_id is not None:
            response = self.client.delete(f'/drinks/{drink_id}')

            self.assertEqual(403, response.status_code)
            data = json.loads(response.data.decode('utf-8'))
            assert_payload_field_type_value(self, data, 'error', int, 403)
            assert_payload_field_type_value(self, data, 'message', str, 'forbidden')
            assert_payload_field_type_value(self, data, 'success', bool, False)

    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_delete_drink_bad_id(self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'barista-token'
        mock_verify_decode_jwt.return_value = {'permissions': ['get:drinks-detail']}

        response = self.client.delete(f'/drinks/{BAD_DRINK_ID}')

        self.assertEqual(403, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'error', int, 403)
        assert_payload_field_type_value(self, data, 'message', str, 'forbidden')
        assert_payload_field_type_value(self, data, 'success', bool, False)


class ManagerUserTest(DeleteDrinksTest):
    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_delete_drink(self, mock_get_token_auth_header, mock_verify_decode_jwt):
        global drink_id

        mock_get_token_auth_header.return_value = 'manager-token'
        mock_verify_decode_jwt.return_value = {'permissions': ['delete:drinks', 'get:drinks-detail', 'patch:drinks', 'post:drinks']}

        if drink_id is not None:
            response = self.client.delete(f'/drinks/{drink_id}')

            self.assertEqual(200, response.status_code)
            data = json.loads(response.data.decode('utf-8'))
            assert_payload_field_type_value(self, data, 'success', bool, True)

    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_delete_drink_bad_id(self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'manager-token'
        mock_verify_decode_jwt.return_value = {'permissions': ['delete:drinks', 'get:drinks-detail', 'patch:drinks', 'post:drinks']}

        response = self.client.delete(f'/drinks/{BAD_DRINK_ID}')

        self.assertEqual(422, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'error', int, 422)
        assert_payload_field_type_value(self, data, 'message', str, 'unprocessable')
        assert_payload_field_type_value(self, data, 'success', bool, False)


