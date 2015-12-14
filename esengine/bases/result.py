# coding: utf-8
import time
import elasticsearch.helpers as eh


class ResultSet(object):
    def __init__(self, values, model, query=None,
                 size=None, es=None, meta=None):
        self._model = model
        self._values = values
        self._query = query
        self._es = model.get_es(es)
        self._size = size
        self._meta = meta
        self._all_values = []

    def __iter__(self):
        return self.values

    @property
    def values(self):
        return (
            self._model.from_dict(dct=value)
            for value in self._values
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
        self._values = [obj['_source'] for obj in resp['hits']['hits']]

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
            eh.bulk(self._es, actions, **meta if meta else {})

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
        eh.bulk(self._es, actions, **meta if meta else {})

    def __unicode__(self):
        return unicode(self.__unicode__())

    def __str__(self):
        return "<ResultSet: {i.values}>".format(i=self)
