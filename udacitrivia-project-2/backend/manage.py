#!venv/bin/python
from flask_script import Manager
from flaskr import create_app

app = create_app()
manager = Manager(app)


@manager.command
def routes():
    print(app.url_map)


if __name__ == "__main__":
    manager.run()
