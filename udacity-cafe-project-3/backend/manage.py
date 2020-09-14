#!python3
from flask_script import Manager
from api import create_app
from api.database.models import db_drop_and_create_all

app = create_app()
manager = Manager(app)


@manager.command
def routes():
    print(app.url_map)

@manager.command
def db_setup():
    db_drop_and_create_all()


if __name__ == "__main__":
    manager.run()
