import json

from models import Category


def test_category_creation(client):
    cat = Category(type='Fancy')

    assert cat.id is None
    assert cat.type == 'Fancy'


def test_category_format(client):
    cat_format = Category(type='Fancy').format()

    assert cat_format['id'] is None
    assert cat_format['type'] == 'Fancy'


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
