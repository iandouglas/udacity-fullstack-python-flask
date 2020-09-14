from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from api.auth.auth import get_token_auth_header, verify_decode_jwt, requires_auth
from flask import Flask, jsonify
from config import config

db = SQLAlchemy()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
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

    # putting flask-restful resource imports here to avoid circular dependencies
    from api.resources.drinks import DrinksResource

    api.add_resource(DrinksResource, '/drinks')

    return app
