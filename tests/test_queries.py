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
            must=[
                Query.bool(
                    must_not=[Query.ids([25, 26])]
                )
            ]
        )
    )
    assert query.as_dict() == raw_query
