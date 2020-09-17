from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException, InternalServerError
from api.auth.auth import get_token_auth_header, verify_decode_jwt, \
    requires_auth, AuthError
from flask import Flask, jsonify
from config import config

db = SQLAlchemy()


class ExtendedAPI(Api):
    """
    credit to https://stackoverflow.com/a/57921890
    adapted the code for the cafe scenario
    This class overrides 'handle_error' method of 'Api' class in Flask-RESTful,
    to extend global exception handing functionality
    """
    def handle_error(self, err):  # pragma: no cover
        """
        prevents writing unnecessary try/except block thoughout the application
        """
        # log every exception raised in the application
        print('API handle_error()', err, err.__class__)

        # catch our custom AuthError
        if isinstance(err, AuthError):
            return jsonify({
                'success': False,
                'error': err.error,
                'code': getattr(err, 'code'),
                'description': getattr(err, 'description'),
            }), err.status_code

        # catch other werkzeug http errors
        if isinstance(err, HTTPException):
            original = getattr(err, "original_exception", None)
            return jsonify({
                'success': False,
                'error': err.code,
                "message": getattr(err.error, 'message')
                }), err.code

        # if 'message' attribute isn't set, assume it's a core Python exception
        if not getattr(err, 'message', None):
            original = getattr(err, "original_exception", None)
            return jsonify({
                'message': 'Server has encountered an unknown error'
                }), 500

        # Handle application-specific custom exceptions
        return jsonify(**err.kwargs), err.http_status_code


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    api = ExtendedAPI(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.errorhandler(InternalServerError)
    @app.errorhandler(500)
    def server_problem(e):
        """
        Example error handling for internal server error
        """
        original = getattr(e, "original_exception", None)
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

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

    @app.errorhandler(403)
    def not_found(error):
        """
        error handler for 403
        """
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden"
        }), 403

    @app.errorhandler(AuthError)
    @app.errorhandler(401)
    def not_found(error):
        """
        error handler for 401
        """
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.route('/auth-required')
    @requires_auth('post:drink')
    def auth_required(payload):
        return jsonify({
            "success": True,
            "message": "authorized"
        }), 200

    # putting flask-restful resource imports here to avoid circular
    # dependencies
    from api.resources.drinks import DrinksResource, DrinkResource, \
        DrinksDetailResource

    api.add_resource(DrinksDetailResource, '/drinks-detail')
    api.add_resource(DrinkResource, '/drinks/<drink_id>')
    api.add_resource(DrinksResource, '/drinks')

    return app
