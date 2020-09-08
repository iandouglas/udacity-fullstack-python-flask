from flask_restful import Resource
from flaskr.resources import get_all_categories


class CategoriesResource(Resource):
    def get(self):
        return get_all_categories()

