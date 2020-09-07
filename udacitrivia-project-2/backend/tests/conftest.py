import pytest
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, g
from models import setup_db


@pytest.fixture(scope='session')
def client():
    app = create_app('testing')
    app.config['TESTING'] = True
    db = setup_db(app, testing=True)

    with app.test_client() as client:
        with app.app_context():
            g.db = db
        yield client


@pytest.fixture(scope='session')
def database():
    app = create_app('testing')
    app.config['TESTING'] = True
    db = setup_db(app, testing=True)

    return db


@pytest.fixture(scope='session')
def _db(database):
    return database
