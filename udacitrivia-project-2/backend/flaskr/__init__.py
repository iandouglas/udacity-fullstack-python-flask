from flask import Flask
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

    # putting flask-restful resource imports here to avoid circular dependencies
    from flaskr.resources.categories import CategoriesResource
    from flaskr.resources.questions import QuestionsResource, QuestionResource

    api.add_resource(CategoriesResource, '/categories')
    api.add_resource(QuestionsResource, '/questions')
    api.add_resource(QuestionResource, '/questions/<int:id>')

    return app
