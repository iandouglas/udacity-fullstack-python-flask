from flask_restful import Resource

from api.database.models import Drink


class DrinksResource(Resource):
    def get(self):
        drinks = Drink.query.order_by(
            Drink.title
        ).all()

        return {
            'success': True,
            'drinks': [drink.short() for drink in drinks]
        }
