import os

import pytest
import requests_mock

from pokespeare.wsgi import create_app


@pytest.fixture(scope="session")
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def m_requests():
    """Mock requests library and yield the instantiated mocker."""
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture(scope="session")
def jsons_path():
    """Return json fixtures directory's path."""
    return f"{os.path.dirname(__file__)}/jsons"
