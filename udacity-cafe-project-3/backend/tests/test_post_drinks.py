import json
import unittest
from copy import deepcopy
from unittest.mock import patch

from api import db, create_app
from tests import db_drop_everything, seed_data, \
    assert_payload_field_type_value, assert_payload_field_type

'''
POST /drinks
    it should create a new row in the drinks table
    it should require the 'post:drinks' permission
    it should contain the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drink} where
    drink an array containing only the newly created drink, or appropriate
    status code indicating reason for failure
'''


class PostDrinksTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db_drop_everything(db)
        db.create_all()
        seed_data(db)

        self.drink_name = 'orange water'
        self.recipe_name_1 = 'red water'
        self.recipe_color_1 = 'red'
        self.recipe_parts_1 = 2
        self.recipe_name_2 = 'yellow water'
        self.recipe_color_2 = 'yellow'
        self.recipe_parts_2 = 3

        self.payload = {
            'title': self.drink_name,
            'recipe': [{
                'name': self.recipe_name_1,
                'color': self.recipe_color_1,
                'parts': self.recipe_parts_1
            }, {
                'name': self.recipe_name_2,
                'color': self.recipe_color_2,
                'parts': self.recipe_parts_2
            }]
        }

    def tearDown(self):
        db.session.remove()
        db_drop_everything(db)
        self.app_context.pop()


class GuestUserTest(PostDrinksTest):
    def test_endpoint_badauth_create_drink(self):
        response = self.client.post('/drinks', json=self.payload,
                                    content_type='application/json')
        self.assertEqual(401, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'error', int, 401)
        assert_payload_field_type_value(self, data, 'message', str,
                                        'unauthorized')
        assert_payload_field_type_value(self, data, 'success', bool, False)


class BaristaUserTest(PostDrinksTest):
    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_badauth_create_drink(
            self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'barista-token'
        mock_verify_decode_jwt.return_value = {
            'permissions': ['get:drinks-detail']
        }

        response = self.client.post('/drinks', json=self.payload,
                                    content_type='application/json')
        self.assertEqual(403, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'error', int, 403)
        assert_payload_field_type_value(self, data, 'message', str,
                                        'forbidden')
        assert_payload_field_type_value(self, data, 'success', bool, False)


# noinspection DuplicatedCode
class ManagerUserTest(PostDrinksTest):
    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_happypath_create_drink_1_ingredient(
            self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'manager-token'
        mock_verify_decode_jwt.return_value = {
            'permissions': ['delete:drinks', 'get:drinks-detail',
                            'patch:drinks', 'post:drinks']
        }

        payload = deepcopy(self.payload)
        payload['recipe'] = payload['recipe'][0]

        response = self.client.post('/drinks', json=payload,
                                    content_type='application/json')
        self.assertEqual(201, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type(self, data, 'drinks', list)

        next_drink = data['drinks'][0]
        assert_payload_field_type(self, next_drink, 'id', int)
        assert_payload_field_type_value(self, next_drink, 'title', str,
                                        self.drink_name)
        assert_payload_field_type(self, next_drink, 'recipe', list)
        self.assertEqual(1, len(next_drink['recipe']))

        next_recipe = next_drink['recipe'][0]
        self.assertIsInstance(next_recipe, dict)
        assert_payload_field_type_value(self, next_recipe, 'name', str,
                                        self.recipe_name_1)
        assert_payload_field_type_value(self, next_recipe, 'color', str,
                                        self.recipe_color_1)
        assert_payload_field_type_value(self, next_recipe, 'parts', int,
                                        self.recipe_parts_1)

    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_happypath_create_drink_2_ingredients(
            self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'manager-token'
        mock_verify_decode_jwt.return_value = {
            'permissions': ['delete:drinks', 'get:drinks-detail',
                            'patch:drinks', 'post:drinks']
        }

        response = self.client.post('/drinks', json=self.payload,
                                    content_type='application/json')
        self.assertEqual(201, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type(self, data, 'drinks', list)

        next_drink = data['drinks'][0]
        assert_payload_field_type(self, next_drink, 'id', int)
        assert_payload_field_type_value(self, next_drink, 'title', str,
                                        self.drink_name)
        assert_payload_field_type(self, next_drink, 'recipe', list)
        self.assertEqual(2, len(next_drink['recipe']))

        next_recipe = next_drink['recipe'][0]
        self.assertIsInstance(next_recipe, dict)
        assert_payload_field_type_value(self, next_recipe, 'name', str,
                                        self.recipe_name_1)
        assert_payload_field_type_value(self, next_recipe, 'color', str,
                                        self.recipe_color_1)
        assert_payload_field_type_value(self, next_recipe, 'parts', int,
                                        self.recipe_parts_1)

        next_recipe = next_drink['recipe'][1]
        self.assertIsInstance(next_recipe, dict)
        assert_payload_field_type_value(self, next_recipe, 'name', str,
                                        self.recipe_name_2)
        assert_payload_field_type_value(self, next_recipe, 'color', str,
                                        self.recipe_color_2)
        assert_payload_field_type_value(self, next_recipe, 'parts', int,
                                        self.recipe_parts_2)

    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_sadpath_create_drink_missing_title(
            self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'manager-token'
        mock_verify_decode_jwt.return_value = {
            'permissions': ['delete:drinks', 'get:drinks-detail',
                            'patch:drinks', 'post:drinks']
        }

        payload = self.payload
        del(payload['title'])

        response = self.client.post('/drinks', json=payload,
                                    content_type='application/json')
        self.assertEqual(400, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(self, data, 'error', str,
                                        'details missing')
        assert_payload_field_type_value(
            self, data, 'message', str,
            'your drink content is missing required data')

    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_sadpath_create_drink_missing_recipe_pieces(
            self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'manager-token'
        mock_verify_decode_jwt.return_value = {
            'permissions': ['delete:drinks', 'get:drinks-detail',
                            'patch:drinks', 'post:drinks']
        }

        self.payload['recipe'].pop()

        # missing entire recipe
        payload = deepcopy(self.payload)
        del(payload['recipe'])

        response = self.client.post('/drinks', json=payload,
                                    content_type='application/json')
        self.assertEqual(400, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(self, data, 'error', str,
                                        'details missing')
        assert_payload_field_type_value(
            self, data, 'message', str,
            'your drink content is missing required data')

        # missing recipe name
        payload = deepcopy(self.payload)
        del(payload['recipe'][0]['name'])

        response = self.client.post('/drinks', json=payload,
                                    content_type='application/json')
        self.assertEqual(400, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(self, data, 'error', str,
                                        'details missing')
        assert_payload_field_type_value(
            self, data, 'message', str,
            'your drink content is missing required data')

        # missing recipe color
        payload = deepcopy(self.payload)
        del(payload['recipe'][0]['color'])

        response = self.client.post('/drinks', json=payload,
                                    content_type='application/json')
        self.assertEqual(400, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(self, data, 'error', str,
                                        'details missing')
        assert_payload_field_type_value(
            self, data, 'message', str,
            'your drink content is missing required data')

        # missing recipe parts
        payload = deepcopy(self.payload)
        del(payload['recipe'][0]['parts'])

        response = self.client.post('/drinks', json=payload,
                                    content_type='application/json')
        self.assertEqual(400, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(
            self, data, 'success', bool, False)
        assert_payload_field_type_value(
            self, data, 'error', str, 'details missing')
        assert_payload_field_type_value(
            self, data, 'message', str,
            'your drink content is missing required data')

    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_endpoint_sadpath_create_title_exists(
            self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'manager-token'
        mock_verify_decode_jwt.return_value = {
            'permissions': ['delete:drinks', 'get:drinks-detail',
                            'patch:drinks', 'post:drinks']
        }

        payload = deepcopy(self.payload)
        payload['recipe'] = payload['recipe'][0]
        response = self.client.post('/drinks', json=payload,
                                    content_type='application/json')
        self.assertEqual(201, response.status_code)

        response = self.client.post('/drinks', json=payload,
                                    content_type='application/json')
        self.assertEqual(422, response.status_code)
