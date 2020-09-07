import os
import sys

from flask import Flask, request, abort, jsonify, flash
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    api = Api(app)
    db = setup_db(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    # TODO Create an endpoint to handle GET requests for all available categories.
    # ./src/components/FormView.js:20:      url: `/categories`, //TODO: update request URL
    # looks for result.categories
    class CategoriesResource(Resource):
        def get(self):
            results = []
            try:
                results = Category.query.order_by(Category.type).all()
            except:
                print(sys.exc_info())
            finally:
                db.session.close()
            return {'categories': [category.format() for category in results]}


    # TODO
    '''
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
  
    ./src/components/QuestionView.js:26:      url: `/questions?page=${this.state.page}`, //TODO: update request URL
    expects result.questions, result.total_questions, result.categories, result.current_category

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    # TODO
    '''
    Create an endpoint to DELETE question using a question ID. 
  
    ./src/components/QuestionView.js:108:          url: `/questions/${id}`, //TODO: update request URL

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    # TODO
    '''
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    ./src/components/FormView.js:37:      url: '/questions', //TODO: update request URL
    sends question, answer, difficulty, category

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    # TODO
    '''
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    ./src/components/QuestionView.js:81:      url: `/questions`, //TODO: update request URL
    sends searchTerm
    expects result.questions, result.total_questions, result.current_category

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    # TODO
    '''
    Create a GET endpoint to get questions based on category. 
  
    ./src/components/QuestionView.js:63:      url: `/categories/${id}/questions`, //TODO: update request URL
    # looks for result.questions array, result.total_questions, result.current_category

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    # TODO
    '''
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    ./src/components/QuizView.js:51:      url: '/quizzes', //TODO: update request URL
    sends previousQuestions, quizCategory
    expects question

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    # TODO
    '''
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    api.add_resource(CategoriesResource, '/categories')
    return app
