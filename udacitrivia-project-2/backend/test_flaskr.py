import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    """
    Requirement:
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_cors(self):
        response = self.client().head('/')

        self.assertIn('Access-Control-Allow-Origin', response.headers)
        self.assertEqual('*', response.headers['Access-Control-Allow-Origin'])
        self.assertIn('Access-Control-Allow-Headers', response.headers)
        self.assertEqual('Content-Type', response.headers['Access-Control-Allow-Headers'])
        self.assertIn('Access-Control-Allow-Methods', response.headers)
        self.assertEqual('GET, PATCH, POST, DELETE, OPTIONS', response.headers['Access-Control-Allow-Methods'])

    def test_get_categories_happypath(self):
        # TODO set up categories
        response = self.client().get('/categories')

        self.assertEqual(200, response.status)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIs(data, list)
        self.assertEquals(3, len(data['results']))

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
