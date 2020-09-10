import json

import bleach
from flask import jsonify, abort, request
from flask_restful import Resource
from sqlalchemy import not_

from flaskr import db
from flaskr.models import Category, Question


class QuizzesResource(Resource):
    def post(self):
        data = json.loads(request.data)
        category = data['quiz_category']['id'].strip()
        previous_questions = data['previous_questions']

        result = None
        if category and category != '0':
            result = db.session.query(Question).filter_by(category=category).filter(not_(Question.id.in_(previous_questions))).first()
        elif category == '0':
            result = db.session.query(Question).filter(not_(Question.id.in_(previous_questions))).first()
        if result is None:
            return {}
        else:
            return {'question': result.format()}
