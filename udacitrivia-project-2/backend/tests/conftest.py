import pytest

from flaskr import create_app


@pytest.fixture
def client():
    app, db = create_app('testing')
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client
