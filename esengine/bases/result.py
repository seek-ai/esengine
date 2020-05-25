# coding: utf-8
import time
import elasticsearch.helpers as eh
from six import text_type

HITS = 'hits'


class ResultSet(object):
    def __init__(self, resp, model, query=None,
                 size=None, es=None, meta=None):
        self._model = model
        self._values = self._hits = resp.get(HITS, {}).get(HITS, [])
        self._query = query
        self._es = model.get_es(es)
        self._size = size or len(self._values)
        self._meta = self._extract_meta(resp)
        if meta:
            self._meta.update(meta)
        self._all_values = []

    def __iter__(self):
        return self.values

    def _extract_meta(self, resp):
        meta = {key: resp[key] for key in resp if key != HITS}
        if HITS in resp:
            hits = resp[HITS]
            meta[HITS] = {key: hits[key] for key in hits if key != HITS}
        return meta

    @property
    def meta(self):
        return self._meta

    @property
    def values(self):
        return (
            self._model.from_es(hit=hit)
            for hit in self._hits
        )

    @property
    def all_values(self):
        if not self._all_values:
            self._all_values = [i for i in self.values]
        return self._all_values

    def __getitem__(self, item):
        return self.all_values[item]

    def reload(self, sleep=1):
        time.sleep(sleep)
        self._all_values = []
        resp = self._es.search(
            index=self._model._index,
            doc_type=self._model._doctype,
            body=self._query,
            size=self._size or len(self._values)
        )
        self._hits = self._values = resp.get('hits', {}).pop('hits', [])
        self._meta = resp
        return resp

    def update(self, meta=None, **kwargs):
        if kwargs:
            actions = [
                {
                    '_op_type': 'update',
                    '_index': self._model._index,
                    '_type': self._model._doctype,
                    '_id': doc.id,
                    'doc': kwargs
                }
                for doc in self.values
            ]
            return eh.bulk(self._es, actions, **meta if meta else {})

    def delete(self, meta=None, **kwargs):
        actions = (
            {
                '_op_type': 'delete',
                '_index': self._model._index,
                '_type': self._model._doctype,
                '_id': doc.id,
            }
            for doc in self.values
        )
        return eh.bulk(self._es, actions, **meta if meta else {})

    def count(self):
        return min(self._size, self.meta.get('hits', {}).get('total')['value'])

    def to_dict(self, *args, **kwargs):
        """
        returns a list of Documents transformed in dicts
        [{}, {}, ...]
        :param args: passed to item
        :param kwargs: passed to item
        :return:
        """
        return [item.to_dict(*args, **kwargs) for item in self.values]

    def get_values(self, *fields):
        """
        if args is only one field .get_values('id') return a list of lists
        [123, 456, 789]
        If args is more than one field return a list of tuples
        .get_values("id", "name")
        [(123, "John"), (789, "mary"), ...]
        :param fields: a list of fields
        :return:
        """
        if not fields:
            raise AttributeError("At least one field is required")

        if len(fields) > 1:
            return [
                tuple(getattr(value, field) for field in fields)
                for value in self.values
            ]
        else:
            return [getattr(value, fields[0]) for value in self.values]

    def __unicode__(self):
        return text_type(self.__unicode__())

    def __str__(self):
        return "<ResultSet: {i.values}>".format(i=self)
