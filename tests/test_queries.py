from esengine.utils.query import BaseQuery, Filter, Query


def test_query_must_not_by_ids():
    raw_query = {
        'query': {
            'bool': {
                'must': [
                    {
                        'bool': {
                            'must_not': [
                                {'ids': {'values': [25, 26]}}
                            ]
                        }
                    }
                ]
            }
        }
    }
    query = BaseQuery(
        query=Query.bool(
            must=[Query.bool(must_not=[Query.ids([25, 26])])]
        )
    )
    assert query.dict == raw_query


def test_filter_must_terms_must_not_ids():
    raw_query = {
        'query': {
            'filtered': {
                'filter': {
                    'bool': {
                        'must': [
                            {'terms': {'field': ['this', 'that', 'other']}}
                        ],
                        'must_not': [{'ids': {'values': [25, 26]}}]
                    }
                }
            }
        }
    }
    query = BaseQuery(
        filter=Filter.bool(
            must=[Filter.terms('field', ['this', 'that', 'other'])],
            must_not=[Filter.ids([25, 26])]
        )
    )
    assert query.dict == raw_query
