import json
import unittest
from unittest.mock import patch

from api import create_app, db
from api.database.models import Drink
from tests import db_drop_everything, seed_data, assert_payload_field_type_value


class DeleteDrinksTest(unittest.TestCase):
    def setUp(self):
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
            }],
            drink_id=1
        )
        drink.insert()
        self.drink_id = drink.id

        self.bad_drink_id = 9872345

    def tearDown(self):
        db.session.remove()
        db_drop_everything(db)
        self.app_context.pop()


# noinspection DuplicatedCode
class GuestUserTest(DeleteDrinksTest):
    def test_endpoint_delete_drink(self):
        response = self.client.delete(f'/drinks/{self.drink_id}')

        self.assertEqual(401, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'error', int, 401)
        assert_payload_field_type_value(self, data, 'message', str, 'unauthorized')
        assert_payload_field_type_value(self, data, 'success', bool, False)

    def test_endpoint_delete_drink_bad_id(self):
        response = self.client.delete(f'/drinks/{self.bad_drink_id}')

        self.assertEqual(401, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'error', int, 401)
        assert_payload_field_type_value(self, data, 'message', str, 'unauthorized')
        assert_payload_field_type_value(self, data, 'success', bool, False)


# noinspection DuplicatedCode
class BaristaUserTest(DeleteDrinksTest):
    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_delete_drink(self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'barista-token'
        mock_verify_decode_jwt.return_value = {'permissions': ['get:drinks-detail']}

        response = self.client.delete(f'/drinks/{self.drink_id}')

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

        response = self.client.delete(f'/drinks/{self.bad_drink_id}')

        self.assertEqual(403, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'error', int, 403)
        assert_payload_field_type_value(self, data, 'message', str, 'forbidden')
        assert_payload_field_type_value(self, data, 'success', bool, False)


class ManagerUserTest(DeleteDrinksTest):
    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_delete_drink(self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'manager-token'
        mock_verify_decode_jwt.return_value = {
            'permissions': ['delete:drinks', 'get:drinks-detail', 'patch:drinks', 'post:drinks']
        }

        response = self.client.delete(f'/drinks/{self.drink_id}')

        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type_value(self, data, 'delete', str, str(self.drink_id))

    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_delete_drink_bad_id(self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'manager-token'
        mock_verify_decode_jwt.return_value = {
            'permissions': ['delete:drinks', 'get:drinks-detail', 'patch:drinks', 'post:drinks']
        }

        response = self.client.delete(f'/drinks/{self.bad_drink_id}')

        self.assertEqual(404, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'error', int, 404)
        assert_payload_field_type_value(self, data, 'message', str, 'resource not found')
        assert_payload_field_type_value(self, data, 'success', bool, False)
