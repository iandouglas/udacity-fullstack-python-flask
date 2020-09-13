from functools import wraps

from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from api.auth.auth import get_token_auth_header, verify_decode_jwt, requires_auth
from api.database.models import setup_db
from flask import Flask, jsonify, abort  # request, abort
from config import config

db = SQLAlchemy()



def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    setup_db(app)
    api = Api(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response

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

    @app.errorhandler(404)
    def not_found(error):
        """
        error handler for 404
        """
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    # TODO implement error handler for AuthError
    '''
    error handler should conform to general task above 
    '''
    @app.errorhandler(401)
    def not_found(error):
        """
        error handler for 401
        """
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 404

    @app.route('/auth-required')
    @requires_auth('post:drink')
    def auth_required(payload):
        print(payload)
        abort(401)

    return app
