from flask_script import Manager
from api import create_app, db
from api.database.models import Drink
from tests import db_drop_everything

app = create_app()
manager = Manager(app)


@manager.command
def routes():
    print(app.url_map)


@manager.command
def db_setup():
    db_drop_everything(db)
    db.create_all()

@manager.command
def db_seed():
    db_drop_everything(db)
    db.create_all()
    drink_1 = Drink(
        'blue water',
        [{
            "name": "Blue Water",
            "color": "blue",
            "parts": 1
        }],
        drink_id=1
    )
    drink_1.insert()

    drink_2 = Drink(
        'green water',
        [{
            "name": "Blue Water",
            "color": "blue",
            "parts": 2
        }, {
            "name": "Yellow Water",
            "color": "yellow",
            "parts": 2
        }],
        drink_id=2
    )
    drink_2.insert()
    db.session.commit()
    print(f'Drink count: {len(db.session.query(Drink).all())}')


if __name__ == "__main__":
    manager.run()
