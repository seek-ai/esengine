from esengine.utils.payload import Payload, Filter, Query


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
    payload = Payload(
        query=Query.bool(
            must=[Query.bool(must_not=[Query.ids([25, 26])])]
        )
    )
    assert payload.dict == raw_query


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
    payload = Payload(
        filter=Filter.bool(
            must=[Filter.terms('field', ['this', 'that', 'other'])],
            must_not=[Filter.ids([25, 26])]
        )
    )
    assert payload.dict == raw_query


def test_arbitrary_arguments_to_query():
    raw_query = {'query': {'bool': {'minimum_should_match': 1}}}
    payload = Payload()
    payload.query(Query.bool(minimum_should_match=1))
    assert payload.dict == raw_query
