import json
import unittest

from flask import Response

from api import create_app, db
from api.auth.auth import AuthError
from tests import db_drop_everything, seed_data, assert_payload_field_type_value


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

        assert_payload_field_type_value(self, data, 'message', str, 'resource not found')
        assert_payload_field_type_value(self, data, 'error', int, 404)
        assert_payload_field_type_value(self, data, 'success', bool, False)

    def test_401_error_no_auth_header(self):
        try:
            self.client.get('/auth-required', headers={})
        except AuthError as e:
            self.assertRaises(AuthError)
            assert_payload_field_type_value(self, e.error, 'code', str, 'authorization_header_missing')
            assert_payload_field_type_value(self, e.error, 'description', str, 'Authorization header is expected.')

    def test_401_error_empty_auth_header(self):
        try:
            self.client.get('/auth-required', headers={'Authorization': '.'})
        except AuthError as e:
            self.assertRaises(AuthError)
            assert_payload_field_type_value(self, e.error, 'code', str, 'invalid_header')
            assert_payload_field_type_value(self, e.error, 'description', str, 'Authorization header must start with "Bearer".')

    def test_401_error_empty_auth_bearer(self):
        try:
            self.client.get('/auth-required', headers={'Authorization': 'Bearer'})
        except AuthError as e:
            self.assertRaises(AuthError)
            assert_payload_field_type_value(self, e.error, 'code', str, 'invalid_header')
            assert_payload_field_type_value(self, e.error, 'description', str, 'Token not found.')

    def test_401_error_bad_auth_bearer(self):
        try:
            self.client.get('/auth-required', headers={'Authorization': 'Bearer foo'})
        except AuthError as e:
            self.assertRaises(AuthError)
            assert_payload_field_type_value(self, e.error, 'code', str, 'invalid_header')
            assert_payload_field_type_value(self, e.error, 'description', str, 'Authorization header must be bearer token.')

    def test_401_error_auth_bearer_too_big(self):
        try:
            self.client.get('/auth-required', headers={'Authorization': 'Bearer foo baz'})
        except AuthError as e:
            self.assertRaises(AuthError)
            assert_payload_field_type_value(self, e.error, 'code', str, 'invalid_header')
            assert_payload_field_type_value(self, e.error, 'description', str, 'Authorization header must be bearer token.')
