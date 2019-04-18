def test_index(client):
    response = client.get('/hue/lights')
    assert response.data