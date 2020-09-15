from sqlalchemy import Column, String, Integer
import json
from api import db


class EmptyClass(object):
    pass


class Drink(db.Model):
    """
    Drink Model
    a persistent drink entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'drinks'

    # Auto-incrementing, unique primary key
    id = Column(Integer, primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color':string, 'name':string, 'parts':number}]
    recipe = Column(String(180), nullable=False)

    def __init__(self, title, recipe_list, drink_id=None):
        self.title = title
        recipe_json = json.dumps(recipe_list)
        self.recipe = recipe_json
        if drink_id is not None:
            self.id = drink_id

    def short(self):
        """
        short form representation of the Drink model
        """
        # print(json.loads(self.recipe))
        short_recipe = [{
            'color': r['color'],
            'parts': r['parts']
        } for r in json.loads(self.recipe)]

        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    def long(self):
        """
        long form representation of the Drink model
        """
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    def insert(self):
        """
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
        """
        db.session.commit()

    def __repr__(self):
        """
        user-friendly printable representation of our object
        """
        return json.dumps(self.short())
