import pytest

from esengine.bases.result import ResultSet
from esengine.bases.result import HITS


def test_resultset_has_values(MockES, INDEX, DOC_TYPE, Doc):
    resp = MockES().search(index=INDEX, doc_type=DOC_TYPE, size=2)
    results = ResultSet(
        resp=resp,
        model=Doc
    )
    assert results._values == [obj for obj in resp['hits']['hits']]
    for result in results:
        assert result.id in MockES().test_ids


def test_get_item_by_index(DocWithDefaultClient, MockES, QUERY):
    results = DocWithDefaultClient.search(QUERY)
    assert results[0].id == MockES().test_ids[0]


def test_get_item_by_index_1(DocWithDefaultClient, MockES, QUERY):
    results = DocWithDefaultClient.search(QUERY)
    assert results[-1].id == MockES().test_ids[-1]


def test_assert_hits():
    assert HITS == 'hits'


def test_resultset_extract_meta(Doc):
    resultset = ResultSet({}, Doc)
    resp = {
        HITS: {
            HITS: '',
            'c': 'd'
        },
        'a': 'a',
        'b': 'c'
    }
    meta = resultset._extract_meta(resp)
    assert meta == {
        'a': 'a',
        'b': 'c',
        HITS: {'c': 'd'}
    }
