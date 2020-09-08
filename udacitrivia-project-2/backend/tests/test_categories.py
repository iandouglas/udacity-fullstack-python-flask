import json
import unittest

from sqlalchemy.exc import IntegrityError

from flaskr import create_app, db
from flaskr.models import Category
from tests import db_drop_everything, seed_data


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
        cat = Category(type='Fancy')
        db.session.add(cat)
        db.session.commit()

        self.assertIsNotNone(cat.id)
        self.assertEqual(cat.type, 'Fancy')

    def test_category_uniqueness_on_type(self):
        cat_2 = None
        try:
            cat_2 = Category(type='Art')
            db.session.add(cat_2)
            db.session.commit()
        except IntegrityError as e:
            self.assertTrue(True)
        finally:
            if cat_2.id is not None:
                self.assertTrue(False, 'we should not be here!!')

    def test_category_format(self):
        cat_format = Category(type='Fancy').format()

        self.assertIsNone(cat_format['id'])
        self.assertEqual(cat_format['type'], 'Fancy')

        cat = Category.query.filter_by(type='Art').one().format()

        self.assertEqual(cat['id'], 2)
        self.assertEqual(cat['type'], 'Art')

    def test_get_categories_happypath(self):
        response = self.client.get('/categories')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('categories', data)
        self.assertIsInstance(data['categories'], list)
        self.assertEqual(6, len(data['categories']))

        first_category = data['categories'][0]
        self.assertIsInstance(first_category, dict)

        self.assertIn('id', first_category)
        self.assertIsInstance(first_category['id'], int)
        self.assertEqual(2, first_category['id'])

        self.assertIn('type', first_category)
        self.assertIsInstance(first_category['type'], str)
        self.assertEqual('Art', first_category['type'])

    def test_get_questions_for_category_happypath(self):
        category = db.session.query(Category).filter_by(type='Entertainment').one()
        response = self.client.get('/categories/{id}/questions'.format(id=category.id))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))

        self.assertIn('total_questions', data)
        self.assertIsInstance(data['total_questions'], int)
        self.assertEqual(3, data['total_questions'])

        self.assertIn('current_category', data)
        self.assertIsNone(data['current_category'])

        self.assertIn('questions', data)
        self.assertIsInstance(data['questions'], list)
        self.assertEqual(3, len(data['questions']))

        first_question = data['questions'][0]
        self.assertIsInstance(first_question, dict)

        self.assertIn('id', first_question)
        self.assertIsInstance(first_question['id'], int)
        self.assertEqual(2, first_question['id'])

        self.assertIn('question', first_question)
        self.assertIsInstance(first_question['question'], str)
        self.assertEqual(first_question['question'], 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?')

        self.assertIn('answer', first_question)
        self.assertIsInstance(first_question['answer'], str)
        self.assertEqual(first_question['answer'], 'Apollo 13')

        self.assertIn('difficulty', first_question)
        self.assertIsInstance(first_question['difficulty'], int)
        self.assertEqual(first_question['difficulty'], 4)

    def test_get_questions_for_category_sadpath_bad_id(self):
        response = self.client.get('/categories/123/questions')

        self.assertEqual(response.status_code, 404)

    def test_get_questions_for_category_sadpath_no_questions(self):
        category = Category(type='testing', id=21)
        db.session.add(category)
        db.session.commit()
        response = self.client.get('/categories/{id}/questions'.format(id=category.id))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))

        self.assertIn('total_questions', data)
        self.assertIsInstance(data['total_questions'], int)
        self.assertEqual(0, data['total_questions'])

        self.assertIn('current_category', data)
        self.assertIsNone(data['current_category'])

        self.assertIn('questions', data)
        self.assertIsInstance(data['questions'], list)
        self.assertEqual(0, len(data['questions']))
