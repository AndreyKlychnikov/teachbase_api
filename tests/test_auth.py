import pytest

from teachbase_api import HttpClient
from teachbase_api.exceptions import AuthError


def test_oauth_login(client_id, client_secret):
    client = HttpClient(client_id=client_id, client_secret=client_secret)
    client.auth()
    assert client.access_token
    assert client.check_token()


def test_access_token(client_id, access_token):
    client = HttpClient(access_token=access_token)
    assert client.check_token()


def test_failed_auth():
    client = HttpClient(access_token="wrong_token")
    with pytest.raises(AuthError):
        client.auth()
