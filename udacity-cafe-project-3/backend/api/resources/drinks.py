import json

from flask import request, jsonify
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from api import requires_auth, db
from api.auth.auth import AuthError
from api.database.models import Drink


class DrinksResource(Resource):
    method_decorators = {
        'post': [requires_auth('post:drinks')]
    }

    def get(self):
        drinks = Drink.query.order_by(
            Drink.title
        ).all()

        return {
            'success': True,
            'drinks': [drink.short() for drink in drinks]
        }, 200

    def post(self, *args, **kwargs):
        """
        allow for one or more ingredients
        (postman only ever sends one, we should allow for more than one)
        {
            "title": "Water3",
            "recipe": {
                "name": "Water",
                "color": "blue",
                "parts": 1
            }
        }

        {
            "title": "Water3",
            "recipe": [{
                "name": "Water",
                "color": "blue",
                "parts": 1
            },{
                "name": "Water",
                "color": "blue",
                "parts": 1
            }]
        }
        """
        data = json.loads(request.data)
        if 'title' in data and 'recipe' in data and \
            (data['recipe'].__class__ == list or data['recipe'].__class__ == dict):
            if data['recipe'].__class__ == dict:
                data['recipe'] = [data['recipe']]
            drink = Drink(data['title'], data['recipe'])
            drink.insert()
            return {
                'success': True,
                'drinks': [drink.long()]
            }, 200


class DrinkResource(Resource):
    method_decorators = {
        'delete': [requires_auth('delete:drinks')]
    }

    def delete(self, *args, **kwargs):
        drink_id = kwargs['drink_id']
        try:
            question = db.session.query(Drink).filter_by(id=drink_id).one()
        except NoResultFound:
            return abort(404)

        question.delete()
        return {
            'success': True,
            'delete': drink_id
        }, 200


class DrinksDetailResource(Resource):
    method_decorators = {
        'get': [requires_auth('get:drinks-detail')]
    }

    def get(self, *args, **kwargs):
        drinks = Drink.query.order_by(
            Drink.title
        ).all()

        return {
            'success': True,
            'drinks': [drink.long() for drink in drinks]
        }, 200
