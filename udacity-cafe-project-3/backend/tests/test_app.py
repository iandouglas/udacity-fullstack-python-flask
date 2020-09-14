import unittest
from functools import wraps
from unittest.mock import patch

from flask import jsonify

from api.auth.auth import AuthError
from tests import db_drop_everything, seed_data, assert_payload_field_type_value


def mock_decorator(perm):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    return decorator


patch('api.auth.auth.requires_auth', mock_decorator).start()
# this create_app import MUST come after the patch above
from api import create_app, db


class AppTest(unittest.TestCase):
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

    def test_cors(self):
        response = self.client.head('/')

        assert_payload_field_type_value(self, response.headers, 'Access-Control-Allow-Origin', str, '*')
        assert_payload_field_type_value(self, response.headers, 'Access-Control-Allow-Headers', str, 'Content-Type')
        assert_payload_field_type_value(self, response.headers, 'Access-Control-Allow-Methods', str, 'GET, PATCH, POST, DELETE, OPTIONS')

    @patch('api.auth.auth.check_permissions')
    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_mock_auth_required_success(self,
                                        mock_get_token_auth_header,
                                        mock_verify_decode_jwt,
                                        mock_check_permissions):
        mock_get_token_auth_header.return_value = 'token-abc123'
        mock_verify_decode_jwt.return_value = {'permissions': ['post:drink']}
        mock_check_permissions.return_value = True

        response = self.client.get('/auth-required', headers={})
        self.assertEqual(200, response.status_code)

    @patch('api.auth.auth.verify_decode_jwt')
    @patch('api.auth.auth.get_token_auth_header')
    def test_mock_auth_required_bad_perm(self, mock_get_token_auth_header, mock_verify_decode_jwt):
        mock_get_token_auth_header.return_value = 'token-abc123'
        mock_verify_decode_jwt.return_value = {'permissions': ['get:drink']}

        # response = self.client.get('/auth-required', headers={})
        response = None
        try:
            response = self.client.get('/auth-required', headers={'Authorization': 'Bearer foo'})
        except AuthError as e:
            self.assertRaises(AuthError)
            assert_payload_field_type_value(self, e.error, 'code', str, 'invalid_header')
            assert_payload_field_type_value(self, e.error, 'description', str, 'Invalid permissions')
        self.assertEqual(403, response.status_code)
