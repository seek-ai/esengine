import pytest

# import elasticsearch.helpers as eh
# from esengine.document import Document
# from esengine.fields import IntegerField, StringField, FloatField
from esengine.exceptions import ClientError


def test_build_result(Doc, MockES):
    resp = MockES().search(index='index', doc_type='doc_type', size=2)
    results = Doc.build_result(resp, es=MockES(), size=2)
    for res in results:
        print res, res.id
        assert res.id in MockES.test_ids


def test_doc_search(Doc, QUERY, MockES):
    docs = Doc.search(QUERY, es=MockES(), size=2)
    for doc in docs:
        assert doc.id in MockES.test_ids


def test_document_save(Doc, MockES):
    Doc(id=MockES.test_id).save(es=MockES())


def test_get_with_id(Doc, MockES):
    assert Doc.get(id=MockES.test_id, es=MockES()).id == MockES.test_id


def test_doc_get(Doc, MockES):
    doc = Doc.get(id=MockES.test_id, es=MockES())
    assert doc.id == MockES.test_id


def test_filter_by_ids(Doc, MockES):
    docs = Doc.filter(ids=MockES.test_ids, es=MockES())
    for doc in docs:
        assert doc.id in MockES.test_ids


def test_raise_if_filter_by_ids_and_filters(Doc, MockES):
    with pytest.raises(ValueError):
        Doc.filter(ids=MockES.test_ids, es=MockES(), filters={"name": "Gonzo"})


def test_update_all(DocWithDefaultClient, QUERY, eh):
    docs = DocWithDefaultClient.search(QUERY, size=2)
    DocWithDefaultClient.update_all(docs, document_id=1)


def test_delete_all(DocWithDefaultClient, QUERY, eh):
    docs = DocWithDefaultClient.search(QUERY, size=2)
    DocWithDefaultClient.delete_all(docs)


def test_save_all(Doc, MockES, eh):
    docs = [
        Doc(id=doc)
        for doc in MockES.test_ids
    ]
    Doc.save_all(docs, es=MockES())


def test_client_not_defined(Doc, MockES):
    doc = Doc(id=MockES.test_id)
    with pytest.raises(ClientError):
        doc.save()

def test_default_client(DocWithDefaultClient, MockES):
    try:
        doc = DocWithDefaultClient(id=MockES.test_id)
        doc.save()
        DocWithDefaultClient.get(id=MockES.test_id)
    except ClientError:
        pytest.fail("Doc has no default connection")


def test_get_es_with_invalid_client(Doc):
    with pytest.raises(ClientError):
        Doc.get_es(int)


def test__es_is_invalid(Doc):
    class DocWithInvalidES(Doc):
        _es = int
    with pytest.raises(ClientError):
        DocWithInvalidES.get_es(None)


def test_unicode_representation(Doc, MockES):
    doc = Doc(id=MockES.test_id)
    assert doc.__unicode__() == u"<D {'id': 100}>"


def test_str_representation(Doc, MockES):
    doc = Doc(id=MockES.test_id)
    assert doc.__str__() == "<D {'id': 100}>"


def test_default_client_injected(Doc, MockES):
    try:
        Doc._es = MockES()
        doc = Doc(id=MockES.test_id)
        doc.save()
        Doc.get(id=MockES.test_id)
    except ClientError:
        pytest.fail("Doc has no default connection")


def test_default_client_injected_as_lambda(Doc, MockES):
    try:
        Doc._es = classmethod(lambda cls: MockES())
        doc = Doc(id=MockES.test_id)
        doc.save()
        Doc.get(id=MockES.test_id)
    except ClientError:
        pytest.fail("Doc has no default connection")


def test_compare_attributed_values_against_fields(DocWithDefaultClient, MockES):
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