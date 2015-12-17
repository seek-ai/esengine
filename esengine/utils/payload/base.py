from esengine.utils.payload.queries import Query
from esengine.utils.payload.meta_util import unroll_struct


class Payload(object):
    _filter = None
    _query = None
    _aggs = []
    _suggesters = []
    _struct = {}

    def __init__(self, **kwargs):
        """
        Normally receives
        :param query: A Query instance
        :param filter: A Filter instance
        :param aggregate: Aggregate instances
        :param suggest: Suggester instances
        :return: Payload Wrapper
        """
        for key, value in kwargs.items():
            if key in ('filter', 'query'):
                setattr(self, key, value)
            else:
                getattr(self, key)(value)

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = query

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, filter_):
        self._filter = filter_

    def aggregate(self, aggregates):
        self._aggs.extend(aggregates)

    def suggest(self, *suggesters):
        self._suggesters.extend(suggesters)

    def set(self, key, value):
        self._struct[key] = value
        return self

    def from_(self, from_):
        self._struct['from'] = from_
        return self

    def fields(self, fields):
        self._struct['_source'] = fields
        return self

    @property
    def dict(self):
        return self.as_dict()

    def as_dict(self):
        if self._filter and self._query:
            self._struct['query'] = Query.filtered(
                filter=self._filter,
                query=self._query
            )

        elif self._filter:
            self._struct['query'] = Query.filtered(
                filter=self._filter
            )

        elif self._query:
            self._struct['query'] = self._query

        if self._aggs:
            aggs = {}
            for agg in self._aggs:
                aggs.update(agg.as_dict())

            self._struct['aggregations'] = aggs

        if self._suggesters:
            suggs = {}
            for sugg in self._suggesters:
                suggs.update(sugg.as_dict())

            self._struct['suggest'] = suggs

        return unroll_struct(self._struct)
