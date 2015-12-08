import elasticsearch.helpers as eh

from esengine.bases.document import BaseDocument
from esengine.bases.metaclass import ModelMetaclass
from esengine.utils import validate_client


class Document(BaseDocument):
    """
    Base Document to be extended in your models definitions

    >>> from elasticsearch import Elasticsearch
    >>> from esengine import Document, StringField
    >>> class MyDoc(Document):
    ...   _autoid = True
    ...   _index = 'indexname'
    ...   _doctype = 'doctypename'
    ...   _mapping = {}
    ...   name = StringField()

    >>> obj = MyDoc(name="Gonzo")
    >>> obj.save(es=Elasticsearch())

    >>> MyDoc.filter(name="Gonzo")

    """

    __metaclass__ = ModelMetaclass
    _autoid = True
    _mapping = {}

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
        """
        Save current instance of a Document

        >>> obj = Document(field='value')
        >>> obj.save()

        :param es: ES client or None (if implemented a default in Model)
        :return: Nothing or raise error
        """
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
    def get(cls, id, es=None, **kwargs):
        """
        A get query returning a single document by _id or _uid

        >>> Document.get(id=123)

        :param id: The _id or _uid of the object
        :param es: ES client or None (if implemented a default in Model)
        :param kwargs: extra key=value to be passed to es client
        :return: A single Doc object
        """
        es = cls.get_es(es)
        res = es.get(index=cls._index,
                     doc_type=cls._doctype,
                     id=id,
                     **kwargs)
        return cls.from_dict(dct=res['_source'])

    @classmethod
    def filter(cls, es=None, ids=None, size=None, **filters):
        """
        A match_all query with filters

        >>> Document.filter(ids=[123, 456])
        >>> Document.filter(name="Gonzo", city="Tunguska", size=10)

        :param es: ES client or None (if implemented a default in Model)
        :param ids: Filtering by _id or _uid
        :param size: size of result, default 100
        :param filters: key=value parameters
        :return: Iterator of Doc objets
        """

        es = cls.get_es(es)

        if ids and not filters:
            filters = {"ids": {"values": list(ids)}}
        else:
            raise ValueError(
                "You can't specify ids together with other filters"
            )

        query = {
            "query": {
                "filtered": {
                    "query": {"match_all": {}},
                    "filter": filters
                }
            }}

        resp = es.search(
            index=cls._index,
            doc_type=cls._doctype,
            body=query,
            size=len(ids) if ids else size
        )

        return cls.build_result(resp)

    @classmethod
    def search(cls, query, es=None, **kwargs):
        """
        Takes a raw ES query in form of a dict and
        return Doc instances iterator

        >>> query = {
        ...     "query": {
        ...        "bool": {
        ...            "must": [
        ...                {"match": {"name": "Gonzo"}}
        ...            ]
        ...        }
        ...    }
        ...}
        >>> results = Document.search(query, size=10)

        :param query: raw query
        :param es: ES client or None (if implemented a default in Model)
        :param kwargs: extra key=value to be passed to es client
        :return: Iterator of Doc objets
        """
        es = cls.get_es(es)
        resp = es.search(
            index=cls._index,
            doc_type=cls._doctype,
            body=query,
            **kwargs
        )
        return cls.build_result(resp)

    @classmethod
    def build_result(cls, resp):
        """
        Takes ES client response having ['hits']['hits']
        and turns it to an generator of Doc objects
        :param resp: ES client raw results
        :return: Generator of Doc objects
        """
        return (
            cls.from_dict(dct=obj['_source']['doc'])
            for obj in resp['hits']['hits']
        )

    @classmethod
    def save_all(cls, docs, es=None):
        """
        Save various Doc instances in bulk

        >>> docs = (Document(value=value) for value in [1, 2, 3])
        >>> Document.save_all(docs)

        :param docs: Iterator of Document instances
        :param es: ES client or None (if implemented a default in Model)
        :return: Nothing or Raise error
        """
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
