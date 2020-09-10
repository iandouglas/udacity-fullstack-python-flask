import json
import unittest
from flaskr import create_app, db
from flaskr.models import Question
from tests import db_drop_everything, seed_data


class QuizTest(unittest.TestCase):
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

    def test_play_quiz_happypath_all_categories_unknown_answer(self):
        """
        6. Create a POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.

        ./src/components/QuizView.js:51:      url: '/quizzes', //TODO: update request URL
        sends previousQuestions, quizCategory
        expects question
        """
        params = {
            "previous_questions": [],
            "quiz_category": {"type": "all", "id": "0"}
        }
        response = self.client.post('/quizzes', json=params)

        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))

        self.assertIn('question', data)
        self.assertIsInstance(data['question'], str)

        self.assertIn('answer', data)
        self.assertIsInstance(data['answer'], str)

        self.assertIn('category', data)
        self.assertIsInstance(data['category'], str)

        self.assertIn('id', data)
        self.assertIsInstance(data['id'], int)

    def test_play_quiz_happypath_all_categories_known_answer(self):
        # in this scenario there's only one possible answer from the database
        params = {
            "previous_questions": [2, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23],
            "quiz_category": {"type": "all", "id": "0"}
        }
        response = self.client.post('/quizzes', json=params)

        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))

        self.assertIn('question', data)
        self.assertIsInstance(data['question'], str)
        self.assertEqual("La Giaconda is better known as what?", data['question'])

        self.assertIn('answer', data)
        self.assertIsInstance(data['answer'], str)
        self.assertEqual("Mona Lisa", data['answer'])

        self.assertIn('category', data)
        self.assertIsInstance(data['category'], str)
        self.assertEqual("2", data['category'])

        self.assertIn('id', data)
        self.assertIsInstance(data['id'], int)
        self.assertEqual(17, data['id'])

    def test_play_quiz_happypath_science_category(self):
        pass

    def test_play_quiz_happypath_no_more_questions(self):
        pass

    def test_play_quiz_sadpath_bad_category(self):
        pass
