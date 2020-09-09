import json

import bleach
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
        errors = []
        good_data = True

        data = json.loads(request.data)
        print('---')
        print('incoming data: (raw)', request.data)
        print('incoming data: (decoded)', data)
        try:
            if data['question'] is None or data['question'].__class__ != str or len(data['question'].strip()) < 1:
                good_data = False
                errors.append('Question text cannot be blank, or was not a string')
        except:
            good_data = False
            errors.append('Question text cannot be blank, or was not a string')

        try:
            if data['answer'] is None or data['answer'].__class__ != str or len(data['answer'].strip()) < 1:
                good_data = False
                errors.append('Answer text cannot be blank, or was not a string')
        except:
            good_data = False
            errors.append('Answer text cannot be blank, or was not a string')

        try:
            if data['difficulty'] is None or data['difficulty'].__class__ != str or int(data['difficulty']) < 1 or int(data['difficulty']) > 5:
                good_data = False
                errors.append('Difficulty integer cannot be blank, and must be an integer between 1 and 5')
        except:
            good_data = False
            errors.append('Difficulty integer cannot be blank, and must be an integer between 1 and 5')

        try:
            if data['category'] is None or data['category'].__class__ != str or db.session.query(Category).filter_by(id=int(data['category'])).one_or_none() is None:
                good_data = False
                errors.append('Category integer cannot be blank, or is set to an invalid category')
        except:
            good_data = False
            errors.append('Category integer cannot be blank, or is set to an invalid category')

        if good_data:
            q = Question(
                question=bleach.clean(data['question']),
                answer=bleach.clean(data['answer']),
                difficulty=bleach.clean(data['difficulty']),
                category=bleach.clean(data['category'])
            )
            db.session.add(q)
            db.session.commit()
            payload = {
                'message': 'New question successfully added',
                'question': q.format()
            }
            return payload, 201

        payload = {
            'message': 'New question was not added, check errors for reasons',
            'errors': errors
        }
        return payload, 400


class QuestionResource(Resource):
    def delete(self, id):
        try:
            question = db.session.query(Question).filter_by(id=id).one()
        except NoResultFound:
            return abort(404, 'Resource not found')
        question.delete()
        return {}, 204

