import elasticsearch.helpers as eh

from es_engine.bases.document import BaseDocument
from es_engine.bases.metaclass import ModelMetaclass
from es_engine.utils import validate_client


class Document(BaseDocument):
    __metaclass__ = ModelMetaclass

    @classmethod
    def get_es(cls, es):
        """
        This proxy-method allows the client overwrite
        and the use of a default client for a document.
        Document transport methods should use cls.get_es(es).method()
        This method also validades that the connection is a valid ES client.
        :return: elasticsearch.ElasticSearch() instance or equivalent client
        """
        validate_client(es)
        return es

    def save(self, es=None):
        doc = self.to_dict()
        self.get_es(es).index(
            index=self.__index__,
            doc_type=self.__doc_type__,
            id=self.id,
            body=doc
        )

    @classmethod
    def get(cls, id=None, ids=None, es=None):
        es = cls.get_es(es)
        if id is not None and ids is not None:
            raise ValueError('id and ids can not be passed together.')
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
                body=query,
                size=len(ids)
            )
            result = []
            for obj in resp['hits']['hits']:
                result.append(cls.from_dict(dct=obj['_source']['doc']))
            return result

    @classmethod
    def save_all(cls, docs, es=None):
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
        eh.bulk(cls.get_es(es), updates)
