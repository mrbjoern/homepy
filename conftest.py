import pytest

from api import create_app


@pytest.fixture
def app():
    print(create_app())
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()