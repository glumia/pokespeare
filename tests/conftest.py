import pytest

from pokespeare.wsgi import create_app


@pytest.fixture(scope="session")
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
