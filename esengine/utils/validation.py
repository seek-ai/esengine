# coding: utf-8

from esengine.exceptions import ClientError


def validate_client(es):
    """
    A valid ES client is a interface which must implements at least
    "index" and "search" public methods.
    preferably an elasticsearch.ElasticSearch() instance
    :param es:
    :return: None
    """

    if not es:
        raise ClientError("ES client cannot be Nonetype")

    try:
        if not callable(es.index) or not callable(es.search) or \
                not callable(es.get):
            raise ClientError(
                "index or search or get Interface is not callable"
            )
    except AttributeError as e:
        raise ClientError(str(e))


class FieldValidator(object):
    def __init__(self):
        self.validation = []

    def validate_value(self, field, value):
        pass

    def validate_item(self, field, item):
        pass

    def __call__(self, field, value):
        self.validate_value(field, value)
        if field._multi:
            [self.validate_item(field, item) for item in value]
        return self.validation
