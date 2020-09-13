from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from api.database.models import setup_db
from flask import Flask, jsonify  # request, abort
from config import config

db = SQLAlchemy()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    setup_db(app)
    api = Api(app)
    # CORS(app)

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

    return app
