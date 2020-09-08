from flask import jsonify
from flask_restful import Resource
from flaskr import db
from flaskr.models import Category, Question
from flaskr.resources import get_all_categories


class CategoriesResource(Resource):
    def get(self):
        return get_all_categories()


class CategoryQuestionsResource(Resource):
    def get(self, id):
        category = db.session.query(Category).filter_by(id=id).one_or_none()
        questions = db.session.query(Question).filter_by(category=str(category.id)).all()

        # if category is None:
        #     return error
        return jsonify({
            'total_questions': len(questions),
            'questions': [question.format() for question in questions],
            'current_category': None
        })
