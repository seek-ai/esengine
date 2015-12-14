import pytest
from esengine.utils import validate_client
from esengine.exceptions import ClientError


class InvalidInterfaceClient(object):
    pass


class InvalidClient(object):
    index = 1
    search = 2
    get = 3


class Client(object):
    def index(self, *args, **kwargs):
        return {"_id": 1, "created": True}

    def search(self, query):
        return query

    def get(self, *args, **kwargs):
        return {"_id": 1}


def test_valid_es_client():
    try:
        validate_client(Client())
    except ClientError as e:
        pytest.fail(e)


def test_raise_on_none_client():
    with pytest.raises(ClientError):
        validate_client(None)


def test_raise_when_invalid_client():
    with pytest.raises(ClientError):
        validate_client(InvalidClient())


def test_client_invalid_interface():
    with pytest.raises(ClientError):
        validate_client(InvalidInterfaceClient())
