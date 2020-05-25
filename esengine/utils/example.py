from elasticsearch import Elasticsearch
from esengine import Document, KeywordField, Payload, Query, Pagination


class Doc(Document):
    _index = 'test'
    _doctype = 'doc'
    _es = Elasticsearch()
    name = KeywordField()


payload = Payload(Doc, query=Query.match_all())
pagination = Pagination(payload, page=1, per_page=5)
