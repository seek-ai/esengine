import elasticsearch.helpers as eh

from esengine.bases.document import BaseDocument
from esengine.bases.metaclass import ModelMetaclass
from esengine.utils import validate_client


class Document(BaseDocument):
    __metaclass__ = ModelMetaclass
    _autoid = True

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
        saved_document = self.get_es(es).index(
            index=self._index,
            doc_type=self._doctype,
            id=self.id,
            body=doc
        )
        if saved_document.get('created'):
            self.id = saved_document['_id']

    @classmethod
    def get(cls, id=None, ids=None, es=None):
        es = cls.get_es(es)
        if id is not None and ids is not None:
            raise ValueError('id and ids can not be passed together.')
        if id is not None:
            res = es.get(index=cls._index,
                         doc_type=cls._doctype,
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
                index=cls._index,
                doc_type=cls._doctype,
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
                '_index': cls._index,
                '_type': cls._doctype,
                '_id': doc.id,
                'doc': doc.to_dict()
            }
            for doc in docs
        ]
        eh.bulk(cls.get_es(es), updates)
