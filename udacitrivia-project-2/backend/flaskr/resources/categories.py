import sys
from flask_restful import Resource
from models import Category

class Categories(Resource):
    def get(self):
        results = Category.query.order_by(Category.type).all()
        return {'categories': [category.format() for category in results]}

