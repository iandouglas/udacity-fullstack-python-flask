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

    def test_play_quiz_happypath_all_categories(self):
        """
        6. Create a POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.

        ./src/components/QuizView.js:51:      url: '/quizzes', //TODO: update request URL
        sends previousQuestions, quizCategory
        expects question
        """

    def test_play_quiz_happypath_science_category(self):
        pass

    def test_play_quiz_happypath_no_more_questions(self):
        pass

    def test_play_quiz_sadpath_bad_category(self):
        pass
