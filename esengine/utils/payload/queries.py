from esengine.utils.payload.meta import BaseFilterQuery, MetaFilterQuery
from esengine.utils.payload.exception import NoQuery

from six import with_metaclass

QUERIES = {
    'match': {
        'field': True,
        'args': ('query',),
        'kwargs': ('operator', 'zero_terms_query', 'cutoff_frequency', 'boost')
    },
    'multi_match': {
        'args': ({'fields': []}, 'query')
    },
    'bool': {
        'kwargs': ({('must', 'must_not', 'should'): ['_query']},)
    },
    'boost': {
        'kwargs': ({('positive', 'negative'): '_query'})
    },
    'common': {
        'args': ('query',),
        'process': lambda q: {'body': q}
    },
    'constant_score': {
        'kwargs': ({'query': '_query', 'filter': '_filter'},)
    },
    'dis_max': {
        'args': ({'queries': ['_query']},)
    },
    'filtered': {
        'kwargs': ({'query': '_query', 'filter': '_filter'},)
    },
    'fuzzy_like_this': {
        'args': ({'fields': []}, 'like_text')
    },
    'fuzzy_like_this_field': {
        'field': True,
        'args': ('like_text',),
        'kwargs': (
            'max_query_terms', 'ignore_tf', 'fuzziness', 'prefix_length',
            'boost', 'analyzer'
        )
    },
    'function_score': {
        'args': ({'functions': []},),
        'kwargs': ({'query': '_query', 'filter': '_filter'},)
    },
    'fuzzy': {
        'field': True,
        'args': ('value',),
        'kwargs': ('boost', 'fuzziness', 'prefix_length', 'max_expansions')
    },
    'geo_shape': {
        'field': True,
        'kwargs': ('type', {'coordinates': []}),
        'field_process': lambda q: {'shape': q}
    },
    'has_child': {
        'args': ('type',),
        'kwargs': ({'query': '_query', 'filter': '_filter'},)
    },
    'has_parent': {
        'args': ('parent_type',),
        'kwargs': ({'query': '_query', 'filter': '_filter'},)
    },
    'ids': {
        'args': ({'values': []},),
        'kwargs': ('type',)
    },
    'indices': {
        'args': ({'indices': []},),
        'kwargs': ({('query', 'no_match_query'): '_query'},)
    },
    'match_all': {
        'kwargs': ('boost',)
    },
    'more_like_this': {
        'args': ({'fields': []}, 'like_text')
    },
    'nested': {
        'args': ('path', {'query': '_query'}),
    },
    'prefix': {
        'field': True,
        'args': ('value',),
        'kwargs': ('boost',)
    },
    'query_string': {
        'args': ('query',),
        'kwargs': ({'fields': []},)
    },
    'simple_query_string': {
        'args': ('query',),
        'kwargs': ({'fields': []},)
    },
    'range': {
        'field': True,
        'kwargs': ('gte', 'gt', 'lte', 'lt',)
    },
    'regexp': {
        'field': True,
        'args': ('value',),
        'kwargs': ('boost', 'flags')
    },
    'span_first': {
        'args': ({'match': '_query'},)
    },
    'span_multi': {
        'args': ({'match': '_query'},)
    },
    'span_near': {
        'args': ({'clauses': ['_query']},)
    },
    'span_not': {
        'kwargs': ({('include', 'exclude'): '_query'},)
    },
    'span_or': {
        'args': ({'clauses': ['_query']},)
    },
    'span_term': {
        'field': True,
        'args': ('value',),
        'kwargs': ('boost',)
    },
    'term': {
        'field': True,
        'args': ('value',),
        'kwargs': ('boost',)
    },
    'terms': {
        'field': True,
        'value_only': True,
        'args': ({'value': ['']},)
    },
    'top_children': {
        'args': ('type',),
        'kwargs': ({'query': '_query'},)
    },
    'wildcard': {
        'field': True,
        'args': ('value',),
        'kwargs': ('boost',)
    }
}


class Query(with_metaclass(MetaFilterQuery, BaseFilterQuery)):
    _ee_type = 'query'
    _definitions = QUERIES
    _exception = NoQuery
