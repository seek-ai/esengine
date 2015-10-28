import elasticsearch.helpers as eh

from es_engine.bases.document import BaseDocument
from es_engine.bases.metaclass import ModelMetaclass


class Document(BaseDocument):
    __metaclass__ = ModelMetaclass

    def save(self, es):
        doc = self.to_dict()
        es.index(index=self.__index__,
                 doc_type=self.__doc_type__,
                 id=self.id,
                 body=doc)

    @classmethod
    def get(cls, es, id=None, ids=None):
        if id is not None and ids is not None:
            raise
        if id is not None:
            res = es.get(index=cls.__index__,
                         doc_type=cls.__doc_type__,
                         id=id)
            return cls.from_dict(dct=res['_source'])
        if ids is not None:
            query = {
                "query": {
                    "filtered": {
                        "query": {"match_all": {}},
                        "filter": {
                            "ids": {
                                "values": list(ids)
                            }
                        }
                    }
                }}
            resp = es.search(
                index=cls.__index__,
                doc_type=cls.__doc_type__,
                body=query
            )
            result = []
            for obj in resp['hits']['hits']:
                result.append(cls.from_dict(dct=obj['_source']['doc']))
            return result

    @classmethod
    def save_all(cls, es, docs):
        updates = [
            {
                '_op_type': 'index',
                '_index': cls.__index__,
                '_type': cls.__doc_type__,
                '_id': doc.id,
                'doc': doc.to_dict()
            }
            for doc in docs
        ]
        eh.bulk(es, updates)
