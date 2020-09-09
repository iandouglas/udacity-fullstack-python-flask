from flask import jsonify, abort
from flask_restful import Resource
from flaskr import db
from flaskr.models import Category, Question


class CategoriesResource(Resource):
    def get(self):
        results = Category.query.order_by(Category.type).all()
        return {'categories': {category.id: category.type for category in results}}


class CategoryQuestionsResource(Resource):
    def get(self, id):
        category = db.session.query(Category).filter_by(id=id).one_or_none()
        if category is None:
            return abort(404, 'Resource not found')

        questions = db.session.query(Question).filter_by(category=str(category.id)).all()
        return jsonify({
            'total_questions': len(questions),
            'questions': [question.format() for question in questions],
            'current_category': None
        })
