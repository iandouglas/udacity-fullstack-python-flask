import json
import unittest
from flaskr import create_app, db
from flaskr.models import Question
from tests import db_drop_everything, seed_data


class QuestionsTest(unittest.TestCase):
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

    def test_get_paginated_questions_page_1(self):
        """
        1. Create an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).

        /questions?page=${this.state.page}
        expects result.questions, result.total_questions, result.categories, result.current_category

        according to https://knowledge.udacity.com/questions/281844 we can ignore current_category and set it to null/None
        """

        for path in ['/questions', '/questions?page=1']:
            response = self.client.get(path)

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode('utf-8'))

            self.assertIn('total_questions', data)
            self.assertIsInstance(data['total_questions'], int)
            self.assertEqual(19, data['total_questions'])

            self.assertIn('categories', data)
            self.assertIsInstance(data['categories'], dict)
            self.assertEqual(6, len(data['categories']))
            categories = data['categories']
            self.assertIn('1', categories)
            self.assertEqual(categories['1'], 'Science')
            self.assertIn('6', categories)
            self.assertEqual(categories['6'], 'Sports')

            self.assertIn('current_category', data)
            assert data['current_category'] is None

            self.assertIn('questions', data)
            self.assertIsInstance(data['questions'], list)
            self.assertEqual(10, len(data['questions']))

            first_question = data['questions'][0]
            self.assertIsInstance(first_question, dict)
            self.assertIn('question', first_question)
            self.assertIsInstance(first_question['question'], str)
            self.assertEqual(first_question['question'], "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?")
            self.assertIn('answer', first_question)
            self.assertIsInstance(first_question['answer'], str)
            self.assertEqual(first_question['answer'], 'Apollo 13')
            self.assertIn('category', first_question)
            self.assertIsInstance(first_question['category'], str)
            self.assertEqual(first_question['category'], '5')
            self.assertIn('difficulty', first_question)
            self.assertIsInstance(first_question['difficulty'], int)
            self.assertEqual(first_question['difficulty'], 4)

    def test_get_paginated_questions_page_2_and_3(self):
        """
        test getting page 2, and page 3 should have no results
        """
        for path in ['/questions?page=2', '/questions?page=3']:
            response = self.client.get(path)

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode('utf-8'))

            self.assertIn('total_questions', data)
            self.assertIsInstance(data['total_questions'], int)
            self.assertEqual(19, data['total_questions'])

            self.assertIn('questions', data)
            self.assertIsInstance(data['questions'], list)

            if path[-1] == '3':
                self.assertEqual(0, len(data['questions']))

            if path[-1] == '2':
                self.assertEqual(9, len(data['questions']))

                first_question = data['questions'][0]
                self.assertEqual(first_question['question'], "The Taj Mahal is located in which Indian city?")

    def test_delete_a_question_happypath(self):
        """
        2. Create an endpoint to DELETE question using a question ID.

        ./src/components/QuestionView.js:108:          url: `/questions/${id}`
        """
        self.assertEqual(db.session.query(Question).count(), 19)
        category_id = 5  # entertainment
        new_q = Question(question="test question", answer="answer", category=str(category_id), difficulty=1)
        db.session.add(new_q)
        db.session.commit()
        self.assertEqual(db.session.query(Question).count(), 20)

        response = self.client.delete('/questions/{id}'.format(id=new_q.id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(db.session.query(Question).count(), 19)

    def test_delete_a_question_sadpath_404(self):
        response = self.client.delete('/questions/0')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('message', data)
        self.assertIsInstance(data['message'], str)
        self.assertEqual(data['message'], 'Resource not found')

    def test_create_new_question_happypath(self):
        my_question = 'this is my question'
        my_answer = 'this is my answer'
        my_difficulty = '4'
        my_category = '2'
        data = {
            'question': my_question,
            'answer': my_answer,
            'difficulty': my_difficulty,
            'category': my_category
        }
        response = self.client.post('/questions', json=data, content_type='application/json')
        self.assertEqual(201, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('message', data)
        self.assertIsInstance(data['message'], str)
        self.assertEqual(data['message'], 'New question successfully added')
        self.assertIn('question', data)
        self.assertIsInstance(data['question'], dict)
        q = data['question']
        self.assertIn('question', q)
        self.assertIsInstance(q['question'], str)
        self.assertEqual(q['question'], my_question)
        self.assertIn('answer', q)
        self.assertIsInstance(q['answer'], str)
        self.assertEqual(q['answer'], my_answer)
        self.assertIn('difficulty', q)
        self.assertIsInstance(q['difficulty'], int)
        self.assertEqual(q['difficulty'], int(my_difficulty))
        self.assertIn('category', q)
        self.assertIsInstance(q['category'], str)
        self.assertEqual(q['category'], my_category)
        self.assertIn('id', q)
        self.assertIsInstance(q['id'], int)
        self.assertGreater(q['id'], 23)

    def test_create_new_question_sadpath_missing_params(self):
        pass

    def test_create_new_question_sadpath_bad_params(self):
        pass

    '''
    3. Create an endpoint to POST a new question,  which will require the question and answer text, category, and difficulty score.
    
    ./src/components/FormView.js:37:      url: '/questions', //TODO: update request URL
    sends question, answer, difficulty, category
    '''

    '''
    4. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
    
    ./src/components/QuestionView.js:81:      url: `/questions`, //TODO: update request URL
    sends searchTerm
    expects result.questions, result.total_questions, result.current_category
    '''

    '''
    6. Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
    
    ./src/components/QuizView.js:51:      url: '/quizzes', //TODO: update request URL
    sends previousQuestions, quizCategory
    expects question
    '''
