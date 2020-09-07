import sys
from flask_restful import Resource
from models import Category


def get_all_categories():
    results = Category.query.order_by(Category.type).all()
    return {'categories': [category.format() for category in results]}


class Categories(Resource):
    def get(self):
        return get_all_categories()

