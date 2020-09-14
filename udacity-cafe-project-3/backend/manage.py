from flask_script import Manager
from api import create_app, db
from api.database.models import setup_db
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


if __name__ == "__main__":
    manager.run()
