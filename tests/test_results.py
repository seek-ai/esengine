import pytest

from esengine.bases.result import ResultSet


def test_resultset_has_values(MockES, INDEX, DOC_TYPE, Doc):
    resp = MockES().search(index=INDEX, doc_type=DOC_TYPE, size=2)
    values=[obj['_source'] for obj in resp['hits']['hits']]
    results = ResultSet(
        values=values,
        model=Doc
    )
    assert results._values == values
    for result in results:
        assert result.id in MockES().test_ids


def test_get_item_by_index(DocWithDefaultClient, MockES, QUERY):
    results = DocWithDefaultClient.search(QUERY)
    assert results[0].id == MockES().test_ids[0]


def test_get_item_by_index_1(DocWithDefaultClient, MockES, QUERY):
    results = DocWithDefaultClient.search(QUERY)
    assert results[-1].id == MockES().test_ids[-1]

