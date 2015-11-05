import pytest

from es_engine.document import Document
from es_engine.fields import IntegerField


class Doc(Document):
        __index__ = 'index'
        __doc_type__ = 'doc_type'
        id = IntegerField()


class MockES(object):
    test_id = 100
    test_ids = [100, 101]

    def index(self, *args, **kwargs):
        assert kwargs['index'] == Doc.__index__
        assert kwargs['doc_type'] == Doc.__doc_type__
        assert kwargs['id'] == self.test_id
        assert 'body' in kwargs

    def get(self, *args, **kwargs):
        assert kwargs['index'] == Doc.__index__
        assert kwargs['doc_type'] == Doc.__doc_type__
        assert kwargs['id'] == self.test_id
        return {
            '_source': {
                'id': self.test_id
            }
        }

    def search(self, *args, **kwargs):
        assert kwargs['index'] == Doc.__index__
        assert kwargs['doc_type'] == Doc.__doc_type__
        assert kwargs['size'] == len(self.test_ids)
        query = {
            "query": {
                "filtered": {
                    "query": {"match_all": {}},
                    "filter": {
                        "ids": {
                            "values": self.test_ids
                        }
                    }
                }
            }
        }
        assert kwargs['body'] == query
        docs = []
        for id in self.test_ids:
            doc = {
                '_source': {
                    'doc': {
                        'id': self.test_id
                    }
                }
            }
            docs.append(doc)
        return {
            'hits': {
                'hits': docs
            }
        }


def test_document_save():
    Doc(id=MockES.test_id).save(MockES())


def test_raise_when_pass_id_and_ids_to_doc_get():
    with pytest.raises(ValueError) as ex:
        Doc.get(MockES(), id=1, ids=[1, 2])
    assert str(ex.value) == 'id and ids can not be passed together.'


def test_doc_get():
    doc = Doc.get(MockES(), id=MockES.test_id)
    assert doc.id == MockES.test_id


def test_doc_get_ids():
    docs = Doc.get(MockES(), ids=MockES.test_ids)
    for doc in docs:
        assert doc.id in MockES.test_ids
