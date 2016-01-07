from esengine.utils.payload.queries import Query
from esengine.utils.payload.meta_util import unroll_struct


class Payload(object):

    def __init__(self, model=None, **kwargs):
        """
        Optional parameters
        :param model: a Document model class (optional)
        :param query: A Query instance
        :param filter: A Filter instance
        :param aggregate: Aggregate instances
        :param suggest: Suggester instances
        :param sort: field name or dictionary
        :param size: Integer size
        :param timeout: Timeout in seconds
        :param fields: List of fields
        :return: Payload Wrapper
        """
        self._model = model
        self._filter = None
        self._query = None
        self._aggs = []
        self._suggesters = []
        self._struct = {}

        for key, value in kwargs.items():
            try:
                getattr(self, key)(value)
            except AttributeError:
                self.set(key, value)

    def query(self, query):
        self._query = query
        return self

    def filter(self, filter_):
        self._filter = filter_
        return self

    def aggregate(self, aggregates):
        self._aggs.extend(aggregates)
        return self

    def suggest(self, *suggesters):
        self._suggesters.extend(suggesters)
        return self

    def set(self, key, value):
        self._struct[key] = value
        return self

    def from_(self, from_):
        self._struct['from'] = from_
        return self

    def size(self, size):
        self._struct['size'] = size
        return self

    def timeout(self, timeout):
        self._struct['timeout'] = timeout
        return self

    def fields(self, fields):
        self._struct['_source'] = fields
        return self

    def sort(self, field, **kwargs):
        if 'sort' not in self._struct:
            self._struct['sort'] = []
        if not kwargs:
            self._struct['sort'].append(field)
        else:
            self._struct['sort'].append({field: kwargs})
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

    # backward compatibility API
    to_dict = as_dict  # noqa

    def search(self, model=None, **kwargs):
        model = model or self._model
        return model.search(query=self.dict, **kwargs)
