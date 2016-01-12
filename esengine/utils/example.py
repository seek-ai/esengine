from elasticsearch import Elasticsearch
from esengine import Document, StringField, Payload, Query, Pagination


class Doc(Document):
    _index = 'test'
    _doctype = 'doc'
    _es = Elasticsearch()
    name = StringField()


payload = Payload(Doc, query=Query.match_all())
pagination = Pagination(payload, page=1, per_page=5)
