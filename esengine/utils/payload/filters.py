from esengine.utils.payload.meta import BaseFilterQuery, MetaFilterQuery
from esengine.utils.payload.exception import NoFilter

from six import with_metaclass


FILTERS = {
    'and_': ['_filter'],
    'bool': {
        'kwargs': ({('must', 'must_not', 'should'): ['_filter']},)
    },
    'exists': {
        'args': ('field',)
    },
    'geo_bounding_box': {
        'field': True,
        'kwargs': ('top_left', 'bottom_right')
    },
    'geo_distance': {
        'field': True,
        'kwargs': ('lat', 'lon')
    },
    'geo_distance_range': {
        'field': True,
        'kwargs': ('lat', 'lon')
    },
    'geo_polygon': {
        'field': True,
        'args': ({'points': []},)
    },
    'geo_shape': {
        'field': True,
        'kwargs': ('type', {'coordinates': []}),
        'field_process': lambda q: {'shape': q}
    },
    'geohash_shell': {
        'field': True,
        'kwargs': ('lat', 'lon',)
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
        'kwargs': ({('filter', 'no_match_filter'): '_filter'},)
    },
    'limit': {
        'args': ('value',)
    },
    'match_all': {},
    'missing': {
        'args': ('field',)
    },
    'nested': {
        'args': ('path', {'filter': '_filter'}),
    },
    'not_': {
        'kwargs': ({'query': '_query', 'filter': '_filter'},)
    },
    'or_': ['_filter'],
    'prefix': {
        'field': True,
        'args': ('value',)
    },
    'range': {
        'field': True,
        'kwargs': ('gte', 'gt', 'lte', 'lt')
    },
    'regexp': {
        'field': True,
        'args': ('value',),
        'kwargs': ('flags', 'max_determinized_states')
    },
    'script': {
        'args': ('script',)
    },
    'term': {
        'field': True,
        'args': ('value',)
    },
    'terms': {
        'field': True,
        'value_only': True,
        'args': ({'value': []},)
    },
    'type': {
        'args': ('value',)
    }
}


class Filter(with_metaclass(MetaFilterQuery, BaseFilterQuery)):
    _ee_type = 'filter'
    _definitions = FILTERS
    _exception = NoFilter

    @classmethod
    def query(cls, query, cache=False):
        if cache:
            return cls('fquery', {
                'query': query,
                '_cache': True
            })
        else:
            return cls('query', query)
