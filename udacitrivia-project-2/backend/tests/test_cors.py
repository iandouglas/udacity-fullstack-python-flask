def test_cors(client):
    response = client.head('/')

    assert 'Access-Control-Allow-Origin' in response.headers
    assert '*' == response.headers['Access-Control-Allow-Origin']
    assert 'Access-Control-Allow-Headers' in response.headers
    assert 'Content-Type' == response.headers['Access-Control-Allow-Headers']
    assert 'Access-Control-Allow-Methods' in response.headers
    assert 'GET, PATCH, POST, DELETE, OPTIONS' == response.headers['Access-Control-Allow-Methods']