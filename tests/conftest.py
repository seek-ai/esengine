# content of conftest.py
import pytest
import elasticsearch.helpers as eh_original
from esengine import Document
from esengine.fields import IntegerField, KeywordField, FloatField

DOUBLE_ID_FIELD = "double_id"

_INDEX = 'index'
_DOC_TYPE = 'doc_type'


class ES(object):
    test_id = 100
    test_ids = [100, 101]

    def index(self, *args, **kwargs):
        assert kwargs['index'] == _INDEX
        assert kwargs['doc_type'] == _DOC_TYPE
        assert kwargs['id'] == self.test_id
        assert 'body' in kwargs
        kwargs['created'] = True
        kwargs['_id'] = self.test_id
        return kwargs

    def get(self, *args, **kwargs):
        assert kwargs['index'] == _INDEX
        assert kwargs['doc_type'] == _DOC_TYPE
        assert kwargs['id'] == self.test_id
        return {
            '_source': {
                'id': self.test_id
            },
            '_id': self.test_id
        }

    def search(self, *args, **kwargs):
        assert kwargs['index'] == _INDEX
        assert kwargs['doc_type'] == _DOC_TYPE
        docs = []
        for _id in self.test_ids:
            doc = {
                '_source': {
                    'id': _id
                },
                '_id': _id,
                '_score': 1.0
            }
            docs.append(doc)
        return {
            'hits': {
                'hits': docs
            }
        }


class ES_fields(object):
    test_id = 100
    test_ids = [100, 101]
    double_ids = [id * 2 for id in test_ids]

    def index(self, *args, **kwargs):
        assert kwargs['index'] == _INDEX
        assert kwargs['doc_type'] == _DOC_TYPE
        assert kwargs['id'] == self.test_id
        assert 'body' in kwargs
        kwargs['created'] = True
        kwargs['_id'] = self.test_id
        return kwargs

    def get(self, *args, **kwargs):
        assert kwargs['index'] == _INDEX
        assert kwargs['doc_type'] == _DOC_TYPE
        assert kwargs['id'] == self.test_id
        return {
            '_source': {
                'id': self.test_id
            },
            '_id': self.test_id
        }

    def search(self, *args, **kwargs):
        assert kwargs['index'] == _INDEX
        assert kwargs['doc_type'] == _DOC_TYPE
        docs = []
        for _id in self.test_ids:
            doc = {
                '_source': {
                    'id': _id
                },
                '_id': _id,
                '_score': 1.0,
                'fields': {
                    "double_id": _id * 2
                }
            }
            docs.append(doc)
        return {
            'hits': {
                'hits': docs
            }
        }


class D(Document):
    _index = _INDEX
    _doctype = _DOC_TYPE
    id = IntegerField()


class DW(D):
    _es = ES()
    id = IntegerField()  # ID hould be inherited
    document_id = KeywordField()
    house_number = IntegerField()
    height = FloatField()


# def pytest_runtest_setup(item):
#     # called for running each test in 'a' directory
#     print("setting up", item)


@pytest.fixture(scope="module")
def INDEX():
    return 'index'


@pytest.fixture(scope="module")
def DOC_TYPE():
    return 'doc_type'


@pytest.fixture(scope="module")
def QUERY():
    return {
        "query": {
            "bool": {
                "must": [
                    {"match": {"name": "Gonzo"}}
                ]
            }
        }
    }


@pytest.fixture(scope="module")
def QUERY_SCRIPT_FIELDS():
    return {
        "query": {
            "match_all": {}
        },
        "script_fields": {
            DOUBLE_ID_FIELD: {"script": "doc[\"id\"]*2"}
        }
    }


@pytest.fixture(scope="module")
def FIELD_NAME():
    return DOUBLE_ID_FIELD


@pytest.fixture(scope="module")
def MockES():
    return ES


@pytest.fixture(scope="module")
def MockESf():
    return ES_fields


@pytest.fixture(scope="module")
def eh():
    def bulk(es, actions):
        for action in actions:
            assert action['_op_type'] in ['index', 'update', 'delete']
            assert action['_index'] == _INDEX
            assert action['_type'] == _DOC_TYPE

    eh_original.bulk = bulk
    return eh_original


@pytest.fixture(scope="module")
def Doc():
    return D


@pytest.fixture(scope="module")
def DocWithDefaultClient():
    return DW
