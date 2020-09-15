from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from api import requires_auth, db
from api.auth.auth import AuthError
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


class DrinkResource(Resource):
    method_decorators = {
        'delete': [requires_auth('delete:drinks')]
    }

    def delete(self, *args, **kwargs):
        drink_id = kwargs['drink_id']
        try:
            question = db.session.query(Drink).filter_by(id=drink_id).one()
        except AuthError:
            return abort(401)
        except NoResultFound:
            return abort(422)

        question.delete()
        return {
            'success': True
        }, 200
