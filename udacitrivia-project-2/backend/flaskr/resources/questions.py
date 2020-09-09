import json

from flask_restful import Resource
from flask import request, abort, current_app
from sqlalchemy.orm.exc import NoResultFound
from flaskr import db
from flaskr.models import Question, Category


class QuestionsResource(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)
        total_count = Question.query.count()
        results = Question.query.order_by(
                Question.id
            ).offset(
                current_app.config['FLASKY_QUESTIONS_PER_PAGE'] * (page-1)
            ).limit(
                current_app.config['FLASKY_QUESTIONS_PER_PAGE']
            ).all()

        category_results = Category.query.order_by(Category.type).all()
        categories = {'categories': [category.format() for category in category_results]}

        return {
            'questions': [question.format() for question in results],
            'total_questions': total_count,
            'categories': {category['id']: category['type'] for category in categories['categories']},
            'current_category': None
        }

    def post(self):
        data = json.loads(request.data)
        q = Question(
            question=data['question'],
            answer=data['answer'],
            difficulty=data['difficulty'],
            category=data['category']
        )
        db.session.add(q)
        db.session.commit()
        payload = {
            'message': 'New question successfully added',
            'question': q.format()
        }
        return payload, 201


class QuestionResource(Resource):
    def delete(self, id):
        try:
            question = db.session.query(Question).filter_by(id=id).one()
        except NoResultFound:
            return abort(404, 'Resource not found')
        question.delete()
        return {}, 204

