from flask_restful import Resource
from flask import request

from flaskr.resources.categories import get_all_categories
from flaskr.models import Question

QUESTIONS_PER_PAGE = 10

class Questions(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)
        total_count = Question.query.count()
        results = Question.query.order_by(
                Question.id
            ).offset(
                QUESTIONS_PER_PAGE * (page-1)
            ).limit(
                QUESTIONS_PER_PAGE
            ).all()
        return {
            'questions': [question.format() for question in results],
            'total_questions': total_count,
            'categories': get_all_categories()['categories'],
            'current_category': None
        }

