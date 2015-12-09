import pytest

from esengine.document import Document
from esengine.fields import IntegerField, StringField, FloatField
from esengine.exceptions import ClientError


QUERY = {
    "query": {
        "bool": {
            "must": [
                {"match": {"name": "Gonzo"}}
            ]
        }
    }
}


class Doc(Document):
        _index = 'index'
        _doctype = 'doc_type'
        id = IntegerField()


class DocWithDefaultClient(Doc):
    id = IntegerField()  # ID hould be inherited
    document_id = StringField()
    house_number = IntegerField()
    height = FloatField()
    @classmethod
    def get_es(cls, es):
        return es or MockES()


class MockES(object):
    test_id = 100
    test_ids = [100, 101]

    def index(self, *args, **kwargs):
        assert kwargs['index'] == Doc._index
        assert kwargs['doc_type'] == Doc._doctype
        assert kwargs['id'] == self.test_id
        assert 'body' in kwargs
        kwargs['created'] = True
        kwargs['_id'] = self.test_id
        return kwargs

    def get(self, *args, **kwargs):
        assert kwargs['index'] == Doc._index
        assert kwargs['doc_type'] == Doc._doctype
        assert kwargs['id'] == self.test_id
        return {
            '_source': {
                'id': self.test_id
            }
        }

    def search(self, *args, **kwargs):
        assert kwargs['index'] == Doc._index
        assert kwargs['doc_type'] == Doc._doctype
        assert kwargs['size'] == len(self.test_ids)
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


def test_build_result():
    resp = MockES().search(index='index', doc_type='doc_type', size=2)
    results = Doc.build_result(resp, es=MockES(), size=2)
    for res in results:
        assert res.id in MockES.test_ids


def test_doc_search():
    docs = Doc.search(QUERY, es=MockES(), size=2)
    for doc in docs:
        assert doc.id in MockES.test_ids


def test_document_save():
    Doc(id=MockES.test_id).save(es=MockES())


def test_get_with_id():
    assert Doc.get(id=MockES.test_id, es=MockES()).id == MockES.test_id


def test_doc_get():
    doc = Doc.get(id=MockES.test_id, es=MockES())
    assert doc.id == MockES.test_id


def test_filter_by_ids():
    docs = Doc.filter(ids=MockES.test_ids, es=MockES())
    for doc in docs:
        assert doc.id in MockES.test_ids


def test_raise_if_filter_by_ids_and_filters():
    with pytest.raises(ValueError):
        Doc.filter(ids=MockES.test_ids, es=MockES(), filters={"name": "Gonzo"})

def mock_bulk(es, updates):
    assert updates == [
        {
            '_op_type': 'index',
            '_index': Doc._index,
            '_type': Doc._doctype,
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


def test_client_not_defined():
    doc = Doc(id=MockES.test_id)
    with pytest.raises(ClientError):
        doc.save()

def test_default_client():
    try:
        doc = DocWithDefaultClient(id=MockES.test_id)
        doc.save()
        DocWithDefaultClient.get(id=MockES.test_id)
    except ClientError:
        pytest.fail("Doc has no default connection")


def test_default_client_injected():
    try:
        Doc._es = MockES()
        doc = Doc(id=MockES.test_id)
        doc.save()
        Doc.get(id=MockES.test_id)
    except ClientError:
        pytest.fail("Doc has no default connection")


def test_default_client_injected_as_lambda():
    try:
        Doc._es = classmethod(lambda cls: MockES())
        doc = Doc(id=MockES.test_id)
        doc.save()
        Doc.get(id=MockES.test_id)
    except ClientError:
        pytest.fail("Doc has no default connection")


def test_compare_attributed_values_against_fields():
    doc = DocWithDefaultClient(id=MockES.test_id)
    doc.document_id = 123456
    doc.house_number = "42"

    with pytest.raises(KeyError):  # invalid field
        doc.name = 'Bruno'
    with pytest.raises(ValueError):  # uncastable
        doc.height = "2 mtrs"

    # TODO: commented asserts will be possible when move to descriptors
    # Because only with descriptors we can overwrite compare methods
    assert doc.house_number == 42
    # assert doc.house_number == "42"
    # assert doc.house_number in ['42']
    assert doc.house_number in [42]
    assert not doc.house_number != 42
    # assert not doc.house_number != "42"
    # assert doc.document_id == 123456
    assert doc.document_id == "123456"
    assert doc.document_id in ['123456']
    # assert doc.document_id in [123456]
    # assert not doc.document_id != 123456
    assert not doc.document_id != "123456"