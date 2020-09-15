import json
import unittest
from unittest.mock import patch

from api import db, create_app
from api.database.models import Drink
from tests import db_drop_everything, seed_data, assert_payload_field_type_value, assert_payload_field_type

'''
GET /drinks-detail
    it should require the 'get:drinks-detail' permission
    it should contain the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
    or appropriate status code indicating reason for failure
'''

class GetAllDrinksDetailTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db_drop_everything(db)
        db.create_all()
        seed_data(db)

        self.drink_1 = Drink(
            'blue water',
            [{
                "name": "Blue Water",
                "color": "blue",
                "parts": 1
            }],
            drink_id=1
        )
        self.drink_1.insert()

        self.drink_2 = Drink(
            'green water',
            [{
                "name": "Blue Water",
                "color": "blue",
                "parts": 2
            }, {
                "name": "Yellow Water",
                "color": "yellow",
                "parts": 2
            }],
            drink_id=2
        )
        self.drink_2.insert()

    def tearDown(self):
        db.session.remove()
        db_drop_everything(db)
        self.app_context.pop()


class GuestUserTest(GetAllDrinksDetailTest):
    def test_endpoint_drinks_happypath_with_drinks(self):
        response = self.client.get('/drinks-detail')
        self.assertEqual(401, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'error', int, 401)
        assert_payload_field_type_value(self, data, 'message', str, 'unauthorized')
        assert_payload_field_type_value(self, data, 'success', bool, False)


class BaristaUserTest(GetAllDrinksDetailTest):
    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_drinks_happypath_with_drinks(self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'barista-token'
        mock_verify_decode_jwt.return_value = {'permissions': ['get:drinks-detail']}

        response = self.client.get('/drinks-detail')
        self.assertEqual(200, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type(self, data, 'drinks', list)

        next_drink = data['drinks'][0]
        assert_payload_field_type_value(self, next_drink, 'id', int, self.drink_1.id)
        assert_payload_field_type_value(self, next_drink, 'title', str, self.drink_1.title)
        assert_payload_field_type(self, next_drink, 'recipe', list)

        next_recipe = next_drink['recipe'][0]
        self.assertIsInstance(next_recipe, dict)
        assert_payload_field_type_value(self, next_recipe, 'name', str, 'Blue Water')
        assert_payload_field_type_value(self, next_recipe, 'color', str, 'blue')
        assert_payload_field_type_value(self, next_recipe, 'parts', int, 1)

        next_drink = data['drinks'][1]
        assert_payload_field_type_value(self, next_drink, 'id', int, self.drink_2.id)
        assert_payload_field_type_value(self, next_drink, 'title', str, self.drink_2.title)
        assert_payload_field_type(self, next_drink, 'recipe', list)
        self.assertEqual(2, len(next_drink['recipe']))

        next_recipe = next_drink['recipe'][0]
        self.assertIsInstance(next_recipe, dict)
        assert_payload_field_type_value(self, next_recipe, 'name', str, 'Blue Water')
        assert_payload_field_type_value(self, next_recipe, 'color', str, 'blue')
        assert_payload_field_type_value(self, next_recipe, 'parts', int, 2)

        next_recipe = next_drink['recipe'][1]
        self.assertIsInstance(next_recipe, dict)
        assert_payload_field_type_value(self, next_recipe, 'name', str, 'Yellow Water')
        assert_payload_field_type_value(self, next_recipe, 'color', str, 'yellow')
        assert_payload_field_type_value(self, next_recipe, 'parts', int, 2)


class ManagerUserTest(GetAllDrinksDetailTest):
    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_drinks_happypath_with_drinks(self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'manager-token'
        mock_verify_decode_jwt.return_value = {'permissions': ['delete:drinks', 'get:drinks-detail', 'patch:drinks', 'post:drinks']}

        response = self.client.get('/drinks-detail')
        self.assertEqual(200, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type(self, data, 'drinks', list)

        next_drink = data['drinks'][0]
        assert_payload_field_type_value(self, next_drink, 'id', int, self.drink_1.id)
        assert_payload_field_type_value(self, next_drink, 'title', str, self.drink_1.title)
        assert_payload_field_type(self, next_drink, 'recipe', list)

        next_recipe = next_drink['recipe'][0]
        self.assertIsInstance(next_recipe, dict)
        assert_payload_field_type_value(self, next_recipe, 'name', str, 'Blue Water')
        assert_payload_field_type_value(self, next_recipe, 'color', str, 'blue')
        assert_payload_field_type_value(self, next_recipe, 'parts', int, 1)

        next_drink = data['drinks'][1]
        assert_payload_field_type_value(self, next_drink, 'id', int, self.drink_2.id)
        assert_payload_field_type_value(self, next_drink, 'title', str, self.drink_2.title)
        assert_payload_field_type(self, next_drink, 'recipe', list)
        self.assertEqual(2, len(next_drink['recipe']))

        next_recipe = next_drink['recipe'][0]
        self.assertIsInstance(next_recipe, dict)
        assert_payload_field_type_value(self, next_recipe, 'name', str, 'Blue Water')
        assert_payload_field_type_value(self, next_recipe, 'color', str, 'blue')
        assert_payload_field_type_value(self, next_recipe, 'parts', int, 2)

        next_recipe = next_drink['recipe'][1]
        self.assertIsInstance(next_recipe, dict)
        assert_payload_field_type_value(self, next_recipe, 'name', str, 'Yellow Water')
        assert_payload_field_type_value(self, next_recipe, 'color', str, 'yellow')
        assert_payload_field_type_value(self, next_recipe, 'parts', int, 2)
