import os

import pytest

from teachbase_api import HttpClient


@pytest.fixture
def access_token():
    return os.getenv("ACCESS_TOKEN")


@pytest.fixture
def client_id():
    return os.getenv("CLIENT_ID")


@pytest.fixture
def client_secret():
    return os.getenv("CLIENT_SECRET")


@pytest.fixture
def client(access_token):
    return HttpClient(access_token=access_token)


@pytest.fixture
def existent_course_id():
    return 55894
