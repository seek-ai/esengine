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
    Doc(id=MockES.test_id).save(es=MockES())


def test_raise_when_pass_id_and_ids_to_doc_get():
    with pytest.raises(ValueError) as ex:
        Doc.get(id=1, ids=[1, 2], es=MockES())
    assert str(ex.value) == 'id and ids can not be passed together.'


def test_doc_get():
    doc = Doc.get(id=MockES.test_id, es=MockES())
    assert doc.id == MockES.test_id


def test_doc_get_ids():
    docs = Doc.get(ids=MockES.test_ids, es=MockES())
    for doc in docs:
        assert doc.id in MockES.test_ids


def mock_bulk(es, updates):
    assert updates == [
        {
            '_op_type': 'index',
            '_index': Doc.__index__,
            '_type': Doc.__doc_type__,
            '_id': doc,
            'doc': {'id': doc}
        }
        for doc in MockES.test_ids
    ]


def test_save_all():
    import elasticsearch.helpers as eh
    eh.bulk = mock_bulk
    docs = [
        Doc(id=doc)
        for doc in MockES.test_ids
    ]
    Doc.save_all(docs, es=MockES())
