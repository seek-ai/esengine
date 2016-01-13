import elasticsearch.helpers as eh

from six import iteritems
from esengine.bases.document import BaseDocument
from esengine.bases.metaclass import ModelMetaclass
from esengine.bases.result import ResultSet
from esengine.mapping import Mapping
from esengine.utils import validate_client
from esengine.utils.payload import Payload, Filter
from esengine.exceptions import ClientError


class Document(BaseDocument):
    """
    Base Document to be extended in your models definitions

    >>> from elasticsearch import Elasticsearch
    >>> from esengine import Document, StringField
    >>> class MyDoc(Document):
    ...   _autoid = True
    ...   _index = 'indexname'
    ...   _doctype = 'doctypename'
    ...   name = StringField()

    >>> obj = MyDoc(name="Gonzo")
    >>> obj.save(es=Elasticsearch())

    >>> MyDoc.filter(name="Gonzo")

    """

    __metaclass__ = ModelMetaclass

    # If _autoid is set to False the id Field will not be automatically
    # included in the Document model and you will need to specify a field
    # called 'id' preferably a StringField
    _autoid = True

    # _validators is a list of callable, each one executed receiving the
    # document instance, and should return None
    # else document is invalid and will not be saved
    # to invalidate the callable should raise validationError or return value
    _validators = None

    @classmethod
    def having(cls, **kwargs):
        meta_attributes = ['index', 'doctype', 'es', 'autoid', 'validators',
                           'strict', 'fields']
        for k, v in kwargs.items():
            setattr(cls, "_" + k if k in meta_attributes else k, v)
        return cls

    @classmethod
    def get_es(cls, es):
        """
        This proxy-method allows the client overwrite
        and the use of a default client for a document.
        Document transport methods should use cls.get_es(es).method()
        This method also validades that the connection is a valid ES client.

        :param es: The Es client or None
        :return: elasticsearch.ElasticSearch() instance or equivalent client
        """
        if not es and hasattr(cls, '_es'):
            es = cls._es if not callable(cls._es) else cls._es()
        validate_client(es)
        return es

    @classmethod
    def refresh(cls, es=None):
        """
        Used to refresh an index and its shards
        Utility for tests purposes

        :param es: ES client
        :return: ES Metadata
        """
        return cls.get_es(es).indices.refresh()

    def save(self, es=None):
        """
        Save current instance of a Document

        >>> obj = Document(field='value')
        >>> obj.save()

        :param es: ES client or None (if implemented a default in Model)
        :return: Es meta data
        """
        doc = self.to_dict()
        saved_document = self.get_es(es).index(
            index=self._index,
            doc_type=self._doctype,
            id=self.id,  # noqa
            body=doc
        )
        created = saved_document.get('created')
        if created:
            self.id = saved_document['_id']
        return saved_document

    def update(self, body=None, es=None, meta=None, **kwargs):
        """
        Update a single document

        Using fields
        >>> Document().update(some_field="some_value")

        Using a body dict
        >>> Document().update({'some_field': "some_value"})

        Or a script
        >>> Document().update(script="for(x in data){x}",
        ...                   lang="groovy",
        ...                   params={'data': [...]})

        :param es: ES client
        :param meta: Extra values to be passed to client
        :param body: Optional values passed as dict
        :param kwargs: values to change
        :return: Update result
        """
        body = body or {}
        body.update(kwargs)
        updated_data = self.update_by_id(
            self.id, body=body, es=es, meta=meta
        )
        if 'script' not in body:
            for key, value in iteritems(body):
                setattr(self, key, value)
        return updated_data

    @classmethod
    def update_by_id(cls, doc_id, body=None, es=None, meta=None, **kwargs):
        """
        Update a single document using its id on BaseClass

        Using fields
        >>> Document.update_by_id(1234, some_field="some_value")
        Using boy dict
        >>> Document.update_by_id(1234, {'some_field': 'some_value'})

        Or a script
        >>> Document.update_by_id(1234,
        ...                       script="for(x in data){x}",
        ...                       lang="groovy",
        ...                       params={'data': [...]})

        :param doc_id: The document of the id to be updated
        :param body: Optional values passed as dict
        :param es: ES client
        :param meta: Extra values to be passed to client
        :param kwargs: values to change
        :return: Update result
        """
        body = body or {}
        body.update(kwargs)
        meta = meta or {}

        if 'script' not in body and 'doc' not in body:
            body = {'doc': body}

        updated_data = cls.get_es(es).update(
            index=cls._index,
            doc_type=cls._doctype,
            id=doc_id,  # noqa
            body=body,
            **meta
        )
        return updated_data

    def delete(self, es=None):
        """
        Delete current instance of a Document

        >>> obj = Document.get(id=123)
        >>> obj.delete()

        :param es: ES client or None (if implemented a default in Model)
        :return: ES meta data
        """
        return self.get_es(es).delete(
            index=self._index,
            doc_type=self._doctype,
            id=self.id,  # noqa
        )

    @classmethod
    def create(cls, es=None, **kwargs):
        """
        Creates and returns an instance of the Document

        >>> Document.create(field='value')
        <Document: {'field': 'value'}>

        :param es: ES client or None (if implemented a default in Model)
        :param kwargs: fields and its values
        :return: Instance of the Document created
        """
        instance = cls(**kwargs)
        instance.save(es)
        return instance

    @classmethod
    def all(cls, *args, **kwargs):
        """
        Returns a ResultSet with all documents without filtering
        A semantic shortcut to filter() without keys

        :param: <See filter parameters>
        :return: A ResultSet with all documents in the index/type
        """
        return cls.filter(*args, **kwargs)

    @classmethod
    def exists(cls, id, es=None, **kwargs):  # noqa
        """
        Tell if document exists on index

        >>> Document.exists(id=123)

        :param id: The _id or _uid of the object
        :param es: ES client or None (if implemented a default in Model)
        :param kwargs: extra key=value to be passed to es client
        :return: True or False
        """
        return cls.get_es(es).exists(
            index=cls._index,
            doc_type=cls._doctype,
            id=id,
            **kwargs
        )

    @classmethod
    def get(cls, id, es=None, **kwargs):  # noqa
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
        return cls.from_es(res)

    @classmethod
    def count_by_query(cls, *args, **kwargs):
        """
        Count documents using a specific raw query
        example: Counting all documents having non-null name field

        >>> query = {
        ...     "query": {
        ...         "filtered": {
        ...             "query": {"match_all": {}},
        ...             "filter": {"exists": {"field": "name"}}
        ...         }
        ...     }
        ... }
        >>> total = Document.count_by_query(query)

        :param args: <see .count parameters>
        :param kwargs: <see .count parameters>
        :return: Integer count
        """
        return cls.count(_method='search', *args, **kwargs)

    @classmethod
    def count(cls, _method='filter', *args, **kwargs):
        """
        Count documents by query or all if no param
        :param args: <see .filter parameters>
        :param _method: filter or search
        :param kwargs: <see .filter parameters>
        :return: Integer count
        """
        kwargs['perform_count'] = True
        return getattr(cls, _method)(*args, **kwargs)

    @classmethod
    def filter(cls, es=None, ids=None,
               size=None, perform_count=False, **filters):
        """
        A match_all query with filters

        >>> Document.filter(ids=[123, 456])
        >>> Document.filter(name="Gonzo", city="Tunguska", size=10)

        :param es: ES client or None (if implemented a default in Model)
        :param ids: Filtering by _id or _uid
        :param size: size of result, default 100
        :param filters: key=value parameters
        :param perform_count: If True, dont return objects, only count
        :return: Iterator of Doc objets
        """

        es = cls.get_es(es)

        if ids and filters:
            raise ValueError(
                "You can't specify ids together with other filters"
            )

        if ids:
            query = {
                "query": {
                    "filtered": {
                        "query": {"match_all": {}},
                        "filter": {"ids": {"values": list(ids)}}
                    }
                }
            }
        elif filters:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {key: value}}
                            for key, value in filters.items()
                        ]
                    }
                }
            }
        else:
            query = {
                "query": {
                    "match_all": {}
                }
            }

        size = len(ids) if ids else size
        search_args = dict(
            index=cls._index,
            doc_type=cls._doctype,
            body=query
        )

        if perform_count:
            return es.count(**search_args)['count']

        if size:
            search_args['size'] = size

        resp = es.search(**search_args)
        return cls.build_result(resp, es=es, query=query, size=size)

    @classmethod
    def search(cls, query, es=None, perform_count=False, **kwargs):
        """
        Takes a raw ES query in form of a dict or Payload and
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

        :param query: raw_query(preferable) or Query or Payload instance
        :param es: ES client or None (if implemented a default in Model)
        :param perform_count: If True, dont return objects, only count
        :param kwargs: extra key=value to be passed to es client
        :return: Iterator of Doc objets

        NOTE: Checking istance types is expensive, please prefer to use
        raw queries ex:
        Document.search({"query": ...}) || .search(payload_instance.dict)
        """

        if not isinstance(query, dict):
            # if not a raw dict query
            if isinstance(query, Payload):  # must be a Payload instance
                query = query.dict
            elif isinstance(query, Filter):  # must be a Filter
                query = Payload(filter=query).dict
            else:  # or a Query to wrap
                query = Payload(query=query).dict

        es = cls.get_es(es)
        search_args = dict(
            index=cls._index,
            doc_type=cls._doctype,
            body=query,
            **kwargs
        )

        if perform_count:
            return es.count(**search_args)['count']

        return cls.build_result(
            es.search(**search_args),
            es=es,
            query=query,
            size=kwargs.get('size')
        )

    @classmethod
    def build_result(cls, resp, query=None, es=None, size=None):
        """
        Takes ES client response having ['hits']['hits']
        and turns it to an generator of Doc objects
        :param resp: ES client raw results
        :param query: The query used to build the results
        :param es: Es client
        :param size: size of results
        :return: ResultSet: a generator of Doc objects
        """

        if resp.get('timed_out'):
            raise ClientError("Timeout")

        return ResultSet(
            resp=resp,
            model=cls,
            query=query,
            size=size,
            es=cls.get_es(es)
        )

    @classmethod
    def save_all(cls, docs, es=None, **kwargs):
        """
        Save various Doc instances in bulk

        >>> docs = (Document(value=value) for value in [1, 2, 3])
        >>> Document.save_all(docs)

        :param docs: Iterator of Document instances
        :param es: ES client or None (if implemented a default in Model)
        :param kwargs: Extra params to be passed to streaming_bulk
        :return: ES metadata
        """
        actions = [
            {
                '_op_type': 'index',
                '_index': cls._index,
                '_type': cls._doctype,
                '_id': doc.id,
                '_source': doc.to_dict()
            }
            for doc in docs
        ]
        return eh.bulk(cls.get_es(es), actions, **kwargs)

    @classmethod
    def update_all(cls, docs, es=None, meta=None, **kwargs):
        """
        Update various Doc instances in bulk

        >>> docs = (Document(value=value) for value in [1, 2, 3])
        # change all values to zero
        >>> Document.update_all(docs, value=0)

        :param docs: Iterator of Document instances
        :param es: ES client or None (if implemented a default in Model)
        :param meta: Extra values to be passed to client
        :param kwargs: Extra params to be passed to streaming_bulk
        :return: Es Metadata
        """
        actions = (
            {
                '_op_type': 'update',
                '_index': cls._index,
                '_type': cls._doctype,
                '_id': doc.id,
                'doc': kwargs
            }
            for doc in docs
        )
        return eh.bulk(cls.get_es(es), actions, **meta if meta else {})

    @classmethod
    def delete_all(cls, docs, es=None, **kwargs):
        """
        Delete various Doc instances in bulk

        >>> docs = (Document(value=value) for value in [1, 2, 3])
        >>> Document.delete_all(docs)

        :param docs: Iterator of Document instances or a list of ids
        :param es: ES client or None (if implemented a default in Model)
        :param kwargs: Extra params to be passed to streaming_bulk
        :return: ES metadata
        """
        actions = [
            {
                '_op_type': 'delete',
                '_index': cls._index,
                '_type': cls._doctype,
                '_id': getattr(doc, 'id', doc),
            }
            for doc in docs
        ]
        return eh.bulk(cls.get_es(es), actions, **kwargs)

    @classmethod
    def random(cls, size=None):
        _query = {
            "query": {
                "function_score": {
                    "query": {"match_all": {}},
                    "random_score": {}
                }
            }
        }
        results = cls.search(_query, size=size)
        return results

    @classmethod
    def put_mapping(cls, *args, **kwargs):
        """
        If index does not exist it is created with mapping
        If exists mapping is updated
        :return: acknowlege
        """
        mapping = Mapping(cls, *args, **kwargs)
        return mapping.save()

    @classmethod
    def init(cls, *args, **kwargs):
        return {
            'mapping': cls.put_mapping(*args, **kwargs),
            'settings': 'Not Implemented yet',
            'analysers': 'Not Implemented yet'
        }

    def __unicode__(self):
        return unicode(self.__str__())

    def __str__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self.to_dict())
