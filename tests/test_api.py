import pytest

from api import create_app


@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get('/hue/lights')
    assert response.data