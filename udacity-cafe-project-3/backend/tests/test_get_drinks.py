import json
import unittest
from unittest.mock import patch

from api import create_app, db
from api.database.models import Drink
from tests import db_drop_everything, seed_data, \
    assert_payload_field_type_value, assert_payload_field_type


class GetAllDrinksTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db_drop_everything(db)
        db.create_all()
        seed_data(db)

    def tearDown(self):
        db.session.remove()
        db_drop_everything(db)
        self.app_context.pop()


# noinspection DuplicatedCode
class GuestUserTest(GetAllDrinksTest):
    def test_endpoint_drinks_happypath_with_drinks(self):
        drink = Drink(
            'blue water',
            [{
                "name": "Water",
                "color": "blue",
                "parts": 1
            }]
        )
        drink.insert()

        response = self.client.get('/drinks')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type(self, data, 'drinks', list)

        first_drink = data['drinks'][0]
        assert_payload_field_type(self, first_drink, 'id', int)
        assert_payload_field_type_value(self, first_drink, 'title', str,
                                        'blue water')
        assert_payload_field_type(self, first_drink, 'recipe', list)

        first_recipe = first_drink['recipe'][0]
        self.assertIsInstance(first_recipe, dict)
        assert_payload_field_type_value(self, first_recipe, 'color', str,
                                        'blue')
        assert_payload_field_type_value(self, first_recipe, 'parts', int, 1)

    def test_endpoint_drinks_happypath_with_no_drinks(self):
        response = self.client.get('/drinks')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type_value(self, data, 'drinks', list, [])


# noinspection DuplicatedCode
class BaristaUserTest(GetAllDrinksTest):
    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_drinks_happypath_with_drinks(
            self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'barista-token'
        mock_verify_decode_jwt.return_value = {
            'permissions': ['get:drinks-detail']
        }
        drink = Drink(
            'blue water',
            [{
                "name": "Water",
                "color": "blue",
                "parts": 1
            }]
        )
        drink.insert()

        response = self.client.get('/drinks')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type(self, data, 'drinks', list)

        first_drink = data['drinks'][0]
        assert_payload_field_type(self, first_drink, 'id', int)
        assert_payload_field_type_value(self, first_drink, 'title', str,
                                        'blue water')
        assert_payload_field_type(self, first_drink, 'recipe', list)

        first_recipe = first_drink['recipe'][0]
        self.assertIsInstance(first_recipe, dict)
        assert_payload_field_type_value(self, first_recipe, 'color', str,
                                        'blue')
        assert_payload_field_type_value(self, first_recipe, 'parts', int, 1)

    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_drinks_happypath_with_no_drinks(
            self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'manager-token'
        mock_verify_decode_jwt.return_value = {
            'permissions': ['delete:drinks', 'get:drinks-detail',
                            'patch:drinks', 'post:drinks']
        }

        response = self.client.get('/drinks')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type_value(self, data, 'drinks', list, [])


# noinspection DuplicatedCode
class ManagerUserTest(GetAllDrinksTest):
    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_drinks_happypath_with_drinks(
            self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'manager-token'
        mock_verify_decode_jwt.return_value = {
            'permissions': ['delete:drinks', 'get:drinks-detail',
                            'patch:drinks', 'post:drinks']
        }

        drink = Drink(
            'blue water',
            [{
                "name": "Water",
                "color": "blue",
                "parts": 1
            }]
        )
        drink.insert()

        response = self.client.get('/drinks')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type(self, data, 'drinks', list)

        first_drink = data['drinks'][0]
        assert_payload_field_type(self, first_drink, 'id', int)
        assert_payload_field_type_value(self, first_drink, 'title', str,
                                        'blue water')
        assert_payload_field_type(self, first_drink, 'recipe', list)

        first_recipe = first_drink['recipe'][0]
        self.assertIsInstance(first_recipe, dict)
        assert_payload_field_type_value(self, first_recipe, 'color', str,
                                        'blue')
        assert_payload_field_type_value(self, first_recipe, 'parts', int, 1)

    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_drinks_happypath_with_no_drinks(
            self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'barista-token'
        mock_verify_decode_jwt.return_value = {
            'permissions': ['get:drinks-detail']
        }

        response = self.client.get('/drinks')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type_value(self, data, 'drinks', list, [])
