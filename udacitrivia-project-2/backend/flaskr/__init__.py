from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    api = Api(app)
    db.init_app(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Cannot process your request'
        }), 422

    # putting flask-restful resource imports here to avoid circular dependencies
    from flaskr.resources.categories import CategoriesResource, CategoryQuestionsResource
    from flaskr.resources.questions import QuestionsResource, QuestionResource, QuestionSearchResource
    from flaskr.resources.quizzes import QuizzesResource

    api.add_resource(CategoriesResource, '/categories')
    api.add_resource(CategoryQuestionsResource, '/categories/<int:id>/questions')
    api.add_resource(QuestionsResource, '/questions')
    api.add_resource(QuestionSearchResource, '/questions/search')
    api.add_resource(QuestionResource, '/questions/<int:id>')
    api.add_resource(QuizzesResource, '/quizzes')

    return app
