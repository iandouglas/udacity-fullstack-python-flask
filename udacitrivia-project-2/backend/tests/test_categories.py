import json

from sqlalchemy.exc import IntegrityError
from flaskr import Category


def test_category_creation(db_session):
    cat = Category(type='Fancy')

    assert cat.id is None
    assert cat.type == 'Fancy'


def test_category_uniqueness_on_type(db_session):
    cat_2 = None
    try:
        cat_2 = Category(type='Art')
        db_session.add(cat_2)
        db_session.commit()
    except IntegrityError as e:
        assert True is True
    finally:
        if cat_2.id is not None:
            assert True is False, 'we should not be here!!'
            Category.query.filter_by(id=cat_2.id).delete()


def test_category_format(db_session):
    cat_format = Category(type='Fancy').format()

    assert cat_format['id'] is None
    assert cat_format['type'] == 'Fancy'

    cat = Category.query.filter_by(type='Art').one().format()

    assert cat['id'] is 2
    assert cat['type'] == 'Art'


def test_get_categories_happypath(client):
    response = client.get('/categories')

    assert '200 OK' == response.status
    data = json.loads(response.data.decode('utf-8'))
    assert 'categories' in data
    assert data['categories'].__class__ == list
    assert 6 == len(data['categories'])

    first_category = data['categories'][0]
    assert first_category.__class__ == dict

    assert 'id' in first_category
    assert first_category['id'].__class__ == int
    assert 2 == first_category['id']

    assert 'type' in first_category
    assert first_category['type'].__class__ == str
    assert 'Art' == first_category['type']
