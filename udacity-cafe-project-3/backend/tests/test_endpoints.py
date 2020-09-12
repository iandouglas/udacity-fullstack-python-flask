import unittest
from api import create_app, db
from tests import db_drop_everything, seed_data
from api.database.models import Drink


class CategoriesTest(unittest.TestCase):
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

    def test_category_creation(self):
        drink = Drink.new
