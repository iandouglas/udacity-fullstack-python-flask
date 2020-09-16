import json

from flask import request, jsonify
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from api import requires_auth, db
from api.auth.auth import AuthError
from api.database.models import Drink


def _validate_single_recipe(recipe):
    proceed = True
    if 'name' not in recipe or 'color' not in recipe or 'parts' not in recipe:
        proceed = False
    return proceed


def _validate_recipe(recipe_data):
    proceed = True
    if recipe_data.__class__ == list:
        for recipe in recipe_data:
            proceed = _validate_single_recipe(recipe)
            if not proceed:
                break
    elif recipe_data.__class__ == dict:
        proceed = _validate_single_recipe(recipe_data)

    return proceed


def _validate_drink(data):
    proceed = True
    if 'title' not in data or 'recipe' not in data:
        proceed = False
    if proceed and 'recipe' in data:
        proceed = _validate_recipe(data['recipe'])
    return proceed


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
        if not _validate_drink(data):
            return {
                'success': False,
                'error': 'details missing',
                "message": 'your drink content is missing required data'
            }, 400

        if data['recipe'].__class__ == list or data['recipe'].__class__ == dict:
            if data['recipe'].__class__ == dict:
                data['recipe'] = [data['recipe']]
            drink = Drink(data['title'], data['recipe'])
            drink.insert()
            return {
                'success': True,
                'drinks': [drink.long()]
            }, 201


class DrinkResource(Resource):
    method_decorators = {
        'delete': [requires_auth('delete:drinks')],
        'patch': [requires_auth('patch:drinks')]
    }

    def delete(self, *args, **kwargs):
        drink_id = kwargs['drink_id']
        try:
            drink = db.session.query(Drink).filter_by(id=drink_id).one()
        except NoResultFound:
            return abort(404)

        drink.delete()
        return {
            'success': True,
            'delete': drink_id
        }, 204

    def patch(self, *args, **kwargs):
        """
        allow for one or more ingredients just like POST
        """
        drink_id = kwargs['drink_id']
        drink = None
        try:
            drink = db.session.query(Drink).filter_by(id=drink_id).one()
        except NoResultFound:
            return abort(404)

        data = json.loads(request.data)
        if 'recipe' in data and not _validate_recipe(data['recipe']):
            return {
                'success': False,
                'error': 'details missing',
                "message": 'your drink content is missing required data'
            }, 400

        if 'title' in data:
            drink.title = data['title']
        if 'recipe' in data:
            if data['recipe'].__class__ == dict:
                data['recipe'] = [data['recipe']]
            drink.recipe = json.dumps(data['recipe'])
        drink.update()

        return {
            'success': True,
            'drinks': [drink.long()]
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
