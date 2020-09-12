# from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from api.database.models import setup_db
from flask import Flask, jsonify  # request, abort
from config import config
# import os
# from sqlalchemy import exc
import json
from flask_cors import CORS
# from .database.models import setup_db  # db_drop_and_create_all, Drink
# from .auth.auth import AuthError, requires_auth


db = SQLAlchemy()


def create_app(config_name='default'):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.errorhandler(422)
    def unprocessable(error):
        """
        Example error handling for unprocessable entity
        """
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    # TODO implement error handlers using the @app.errorhandler(error) decorator
    '''
    each error handler should return (with appropriate messages):
     jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
            }), 404
    '''

    # TODO implement error handler for 404
    '''
    error handler should conform to general task above 
    '''

    # TODO implement error handler for AuthError
    '''
    error handler should conform to general task above 
    '''


'''
# uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# TODO better yet, move this to a cmdline script as we shouldn't have to tweak code to mitigate this
# db_drop_and_create_all()

# ROUTES
# TODO implement endpoint, GET /drinks
'''
GET /drinks
    it should be a public endpoint
    it should contain only the drink.short() data representation
returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
    or appropriate status code indicating reason for failure
'''

# TODO implement endpoint, GET /drinks-detail
'''
GET /drinks-detail
    it should require the 'get:drinks-detail' permission
    it should contain the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
    or appropriate status code indicating reason for failure
'''

# TODO implement endpoint, POST /drinks
'''
POST /drinks
    it should create a new row in the drinks table
    it should require the 'post:drinks' permission
    it should contain the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
    or appropriate status code indicating reason for failure
'''

# TODO implement endpoint, PATCH /drinks/<id>
'''
PATCH /drinks/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should update the corresponding row for <id>
    it should require the 'patch:drinks' permission
    it should contain the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
    or appropriate status code indicating reason for failure
'''

# TODO implement endpoint, DELETE /drinks/<id>
'''
DELETE /drinks/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should delete the corresponding row for <id>
    it should require the 'delete:drinks' permission
returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
    or appropriate status code indicating reason for failure
'''

